
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Diretório para salvar os gráficos
static_directory = os.path.join(os.getcwd(), 'static')

def generate_plot(save_directory):
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
