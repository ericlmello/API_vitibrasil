import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Diretório dos arquivos CSV
save_directory = Config.ASSETS_DIR  # Certifique-se de que esta variável está definida no seu arquivo de configuração
# Caminho para a pasta 'static'
static_directory = os.path.join(os.getcwd(), 'static')
# Função para gerar e salvar o gráfico na pasta 'static'
def generate_plot():
    # Carregar os dados CSV
    importacao_df = pd.read_csv(f'{save_directory}/Importacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    exportacao_df = pd.read_csv(f'{save_directory}/Exportacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    producao_df = pd.read_csv(f'{save_directory}/Producao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    comercializacao_df = pd.read_csv(f'{save_directory}/Comercializacao.csv', sep=';', on_bad_lines='skip', encoding='utf-8')
    processamento_df = pd.read_csv(f'{save_directory}/Processamento.csv', sep=';', on_bad_lines='skip', encoding='utf-8')

    # Processar dados
    for df in [importacao_df, exportacao_df, producao_df, comercializacao_df, processamento_df]:
        df.columns = df.columns.str.strip()

    for year in ['2020', '2021', '2022', '2023']:
        for df in [importacao_df, exportacao_df, producao_df, comercializacao_df, processamento_df]:
            df[year] = pd.to_numeric(df[year].str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')

    importacao_df['Tipo'] = 'Importação'
    exportacao_df['Tipo'] = 'Exportação'
    producao_df['Tipo'] = 'Produção'
    comercializacao_df['Tipo'] = 'Comercialização'
    processamento_df['Tipo'] = 'Processamento'

    df = pd.concat([importacao_df, exportacao_df, producao_df, comercializacao_df, processamento_df], ignore_index=True)
    df = df[df['País'] != 'Total']

    df_grouped = df.groupby(['País', 'Tipo'], as_index=False)[['2020', '2021', '2022', '2023']].sum()
    df_importacao = df_grouped[df_grouped['Tipo'] == 'Importação'].sort_values(by='2022', ascending=False)
    top_paises_importacao = df_importacao['País'].head(10)
    df_filtered = df_grouped[df_grouped['País'].isin(top_paises_importacao)]

    # Criar o gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x='País', y='2022', hue='Tipo', data=df_filtered, order=top_paises_importacao)
    plt.yscale('log')
    plt.xticks(rotation=45, ha='right')
    plt.title('Comparação de Importação, Exportação, Produção, Comercialização e Processamento - Top 10 Países (2022)')
    plt.xlabel('País')
    plt.ylabel('Quantidade (Kg) [escala logarítmica]')
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Caminho para a pasta 'static'
    static_directory = os.path.join(os.getcwd(), 'static')

    # Verificar se o diretório existe, se não, criá-lo
    if not os.path.exists(static_directory):
        os.makedirs(static_directory)

    # Salvar o gráfico na pasta 'static' como graph.png
    plt.savefig(os.path.join(static_directory, 'graph.png'))
    plt.close()

    return os.path.join(static_directory, 'graph.png')  # Retorna o caminho do gráfico salvo
