import os

class Config:
    JWT_SECRET_KEY = 'super-secret-key'
    ASSETS_DIR = 'assets'

    # Lista de arquivos CSV para download
    FILES = [
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02', 'name': 'Producao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03', 'name': 'Processamento.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04', 'name': 'Comercializacao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05', 'name': 'Importacao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06', 'name': 'Exportacao.csv'},
    ]

    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
