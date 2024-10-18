from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_jwt_extended import JWTManager, jwt_required
import logging
from flasgger import Swagger
from config import Config
from download import download_file, read_csv_as_html_table, download_csv
from auth import login
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO
from utils import  corrigir_csv_somando_duplicadas, gerar_dimensao_pais
from plot_generator import generate_plot

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
jwt = JWTManager(app)
swagger = Swagger(app)  # Inicializa o Flasgger

# Diretório dos arquivos CSV
save_directory = Config.ASSETS_DIR  # Certifique-se de que esta variável está definida no seu arquivo de configuração
# Caminho para a pasta 'static'
static_directory = os.path.join(os.getcwd(), 'static')

# Verificação de diretórios e contexto de execução
print(f'Save directory: {save_directory}')
print(f'Static directory: {static_directory}')
print(f'Current working directory: {os.getcwd()}')

# Função para gerar e salvar o gráfico na pasta 'static'
def generate_plot():
    # Carregar os dados CSV
    importacao_df = pd.read_csv(f'{save_directory}/Importacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    exportacao_df = pd.read_csv(f'{save_directory}/Exportacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    producao_df = pd.read_csv(f'{save_directory}/Producao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    comercializacao_df = pd.read_csv(f'{save_directory}/Comercializacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    processamento_df = pd.read_csv(f'{save_directory}/Processamento.csv', sep=';', on_bad_lines='skip', encoding='utf-8')

    # Adicionar a coluna 'Tipo' para diferenciar os dados
    importacao_df['Tipo'] = 'Importação'
    exportacao_df['Tipo'] = 'Exportação'
    producao_df['Tipo'] = 'Produção'
    comercializacao_df['Tipo'] = 'Comercialização'
    processamento_df['Tipo'] = 'Processamento'
    
    # Combinar todos os DataFrames
    df = pd.concat([importacao_df, exportacao_df, producao_df, comercializacao_df, processamento_df], ignore_index=True)
    df = df[df['País'] != 'Total']
    
    # Encontrar o último ano presente nas colunas
    anos_disponiveis = [col for col in df.columns if col.isdigit()]
    ultimo_ano = max(anos_disponiveis)
    
    # Agrupar e somar os dados pelos países e tipos de operação
    df_grouped = df.groupby(['País', 'Tipo'], as_index=False)[anos_disponiveis].sum()
    
    # Filtrar para os 10 principais países em importação no último ano
    df_importacao = df_grouped[df_grouped['Tipo'] == 'Importação'].sort_values(by=ultimo_ano, ascending=False)
    top_paises_importacao = df_importacao['País'].head(10)
    df_filtered = df_grouped[df_grouped['País'].isin(top_paises_importacao)]
    
    # Criar o gráfico com os dados do último ano
    plt.figure(figsize=(12, 6))
    sns.barplot(x='País', y=ultimo_ano, hue='Tipo', data=df_filtered, order=top_paises_importacao)
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Comparação de Importação e Exportação - Top 10 Países ({ultimo_ano})')
    plt.yscale('log')
    plt.xlabel('País')
    plt.ylabel('Quantidade (Kg) [escala logarítmica]')
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Verificar se o diretório 'static' existe, senão criá-lo
    if not os.path.exists(static_directory):
        os.makedirs(static_directory)

    # Salvar o gráfico na pasta 'static'
    graph_path = os.path.join(static_directory, 'graph.png')
    plt.savefig(graph_path)
    plt.close()

    return graph_path


@app.route('/analises', methods=['GET'])
def analises():
    """
    Visualizar gráfico de análise de dados
    ---
    tags:
      - Analises
    responses:
      200:
        description: Gráfico gerado com sucesso
    """
    graph_url = generate_plot()  # Gere o gráfico e obtenha o caminho
    return jsonify({"url": graph_url}), 200  # Retorna a URL do gráfico

# Função para download do arquivo de dimensão País
@app.route('/download/dimensao_pais', methods=['GET'])
def download_dimensao_pais():
    try:
        # Gera o CSV de dimensão País em memória
        csv_content = gerar_dimensao_pais()

        # Envia o arquivo CSV gerado diretamente como anexo
        return send_file(csv_content, as_attachment=True, download_name='dimensao_pais.csv', mimetype='text/csv')
    except Exception as e:
        logging.error(f"Erro ao enviar o arquivo: {e}")
        abort(500, description="Erro ao enviar o arquivo.")


# Endpoint para download do arquivo CSV
@app.route('/download/<file_type>', methods=['GET'])
@jwt_required()
def download(file_type):
    """
    Download de Arquivo
    ---
    tags:
      - Files
    parameters:
      - name: file_type
        in: path
        type: string
        required: true
        description: Tipo de arquivo a ser baixado
    responses:
      200:
        description: Arquivo CSV baixado com sucesso
      401:
        description: Token inválido ou expirado
      404:
        description: Arquivo não encontrado
    """
    return download_file(file_type)


# Endpoint para visualizar o arquivo CSV como uma tabela HTML
@app.route('/view_csv/<file_type>', methods=['GET'])
@jwt_required()
def view_csv(file_type):
    """
    Visualizar arquivo CSV como tabela HTML
    ---
    tags:
      - Files
    parameters:
      - name: file_type
        in: path
        type: string
        required: true
        description: Tipo de arquivo CSV a ser visualizado
    responses:
      200:
        description: Tabela HTML com os dados do arquivo CSV
      404:
        description: Arquivo não encontrado
    """
    table_html = read_csv_as_html_table(file_type)
    if table_html:
        return jsonify({'table_html': table_html}), 200
    return jsonify({"msg": "Arquivo não encontrado"}), 404


# Endpoint de login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Login
    ---
    tags:
      - Auth
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: Nome de usuário
      - name: password
        in: body
        type: string
        required: true
        description: Senha
    responses:
      200:
        description: Login bem-sucedido, retorna o token de acesso
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token de acesso
      401:
        description: Credenciais inválidas
    """
    if request.method == 'POST':
        return login()  # Chama a função de login quando o formulário é enviado
    return render_template('login.html')  # Retorna o formulário de login em GET


if __name__ == '__main__':
    app.run(debug=False)

