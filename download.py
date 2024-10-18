import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import logging
import pandas as pd
from flask import send_file, abort
from config import Config

def download_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('span', class_='spn_small')
        if download_button:
            download_link = download_button.find_parent('a')['href']
            csv_response = requests.get(requests.compat.urljoin(url, download_link))
            csv_response.raise_for_status()
            return csv_response.content
        else:
            return None
    except requests.RequestException:
        return None


def download_file(file_type):
    try:
        file_info = next((item for item in Config.FILES if item['name'].lower().startswith(file_type.lower())), None)
        if not file_info:
            abort(404, description="Arquivo não encontrado.")

        logging.info(f"Baixando o arquivo: {file_info['name']}")
        csv_content = download_csv(file_info['url'])

        if not csv_content:
            logging.error(f"Conteúdo CSV não encontrado para o arquivo: {file_info['name']}")
            abort(404, description="Arquivo não encontrado.")

        file_path = os.path.join(Config.ASSETS_DIR, file_info['name'])
        with open(file_path, 'wb') as f:
            f.write(csv_content)

        logging.info(f"Arquivo salvo em: {file_path}")
        return send_file(
            BytesIO(csv_content),
            as_attachment=True,
            download_name=file_info['name']
        )

    except Exception as e:
        logging.error(f"Erro ao processar download: {e}")
        abort(500, description="Erro interno do servidor.")



def read_csv_as_html_table(file_type):
    # Buscar informações do arquivo com base no tipo
    file_info = next((item for item in Config.FILES if item['name'].lower().startswith(file_type.lower())), None)
    if not file_info:
        return None

    file_path = os.path.join(Config.ASSETS_DIR, file_info['name'])
    
    # Baixar o arquivo CSV se ele não existir localmente
    if not os.path.exists(file_path):
        csv_content = download_csv(file_info['url'])
        if csv_content:
            with open(file_path, 'wb') as f:
                f.write(csv_content)

    try:
        # Lê o CSV com separador ";"
        df = pd.read_csv(file_path, sep=';')

        # Remover a coluna "control" se o arquivo for de Processamento, Producao ou Comercializacao
        if file_type.lower() in ['processamento', 'producao', 'comercializacao']:
            if 'control' in df.columns:
                df.drop(columns=['control'], inplace=True)

        # Substituir valores NaN por 0
        df.fillna(0, inplace=True)

        # Identificar colunas com ".1" (duplicadas) e somar com a coluna original
        for col in df.columns:
            if '.1' in col:
                original_col = col.split('.')[0]
                if original_col in df.columns:
                    df[original_col] += df[col]
                df.drop(columns=[col], inplace=True)

        # Converter o DataFrame para HTML
        return df.to_html(classes='table table-striped', index=False)

    except Exception as e:
        logging.error(f"Erro ao ler o arquivo CSV: {e}")
        return None


