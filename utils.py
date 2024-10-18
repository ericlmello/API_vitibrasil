import pandas as pd
from io import BytesIO
from download import download_csv
import os
import matplotlib.pyplot as plt
import seaborn as sns

static_directory = os.path.join(os.getcwd(), 'static')

# Função para gerar o CSV de dimensão País (sem salvar no disco)
def gerar_dimensao_pais():
    try:
        print("Baixando arquivo de importação...")
        importacao_csv = download_csv('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05')
        print("Baixando arquivo de exportação...")
        exportacao_csv = download_csv('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06')

        if not importacao_csv or not exportacao_csv:
            print("Erro: Arquivos não baixados corretamente")
            return None

        # Corrigir e carregar os arquivos em dataframes
        print("Corrigindo e carregando arquivos...")
        df_importacao = corrigir_csv_somando_duplicadas(importacao_csv)
        df_exportacao = corrigir_csv_somando_duplicadas(exportacao_csv)
        print("Arquivos carregados e corrigidos com sucesso!")

        # Combinar as colunas de "País", remover duplicatas e criar coluna "id"
        paises = pd.concat([df_importacao[['País']], df_exportacao[['País']]]).drop_duplicates().reset_index(drop=True)
        paises['id'] = paises.index + 1

        # Criar o arquivo CSV em memória
        output = BytesIO()
        paises.to_csv(output, index=False, columns=['id', 'País'], encoding='utf-8')
        output.seek(0)

        print("CSV de dimensão país gerado com sucesso!")
        return output
    except Exception as e:
        print(f"Erro ao gerar dimensão país: {e}")
        return None

# Função para somar colunas duplicadas
def corrigir_csv_somando_duplicadas(csv_data):
    df = pd.read_csv(BytesIO(csv_data), sep=';')
    df = df.groupby(df.columns, axis=1).sum()
    return df
