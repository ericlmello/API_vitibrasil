# Tech Challenge  
## Projeto de API - Vitibrasil  

### Descrição Geral:  
O projeto **vitibrasil** é uma aplicação web desenvolvida com Flask que centraliza e gerencia dados sobre a produção, importação, exportação, comercialização e processamento de produtos de diversos países. Ele permite que usuários autenticados façam o download de arquivos CSV, visualizem dados como tabelas HTML e gerem gráficos comparativos para análise dos principais países. O sistema também oferece uma funcionalidade para geração dinâmica de um arquivo CSV consolidado chamado **"Dimensão País"**, útil para análises exploratórias e preditivas.

### Funcionalidades Principais:  
1. **Autenticação com JWT (JSON Web Token):**  
   - Autenticação por nome de usuário e senha para geração de token JWT.  
   - O token é necessário para acessar as funcionalidades da API.

2. **Download de Arquivos CSV:**  
   - Arquivos CSV contendo dados de produção, processamento, importação, exportação e **Dimensão País**.  
   - Os arquivos são baixados diretamente após o login.  

3. **Visualização de Arquivos CSV como Tabelas:**  
   - Visualização de dados CSV no navegador como tabelas HTML interativas.

4. **Geração de Gráficos:**  
   - Gráficos de comparação para as principais métricas de produção, importação, exportação, comercialização e processamento para os 10 maiores países em 2023.

5. **Geração e Download de "Dimensão País":**  
   - CSV consolidado com dados agregados de importação e exportação, útil para análises mais aprofundadas.

6. **Documentação Automática com Swagger:**  
   - Documentação automática dos endpoints da API para facilitar o uso e teste.

### Cenários de Uso:
1. **Análise de Comércio Internacional:**  
   Empresas e pesquisadores podem analisar dados econômicos de diferentes países.  

2. **Comparação de Métricas Entre Países:**  
   Gráficos de comparação para identificar os maiores importadores/exportadores.  

3. **Consultoria Econômica:**  
   Análises com base no arquivo **Dimensão País** consolidado.

4. **Download e Processamento de Dados:**  
   Arquivos CSV disponíveis para uso externo em relatórios ou integrações.

### Funcionalidades Futuras:  
- **Data Lake Automatizado:** Repositório centralizado para armazenar dados atualizados de fontes externas.
- **Dashboards Interativos:** Visualização em tempo real de dados comerciais.
- **Detecção de Anomalias:** Modelos de machine learning para identificar padrões incomuns.
- **Classificação de Países:** Classificação de países com base em indicadores econômicos.
- **Previsão de Tendências de Importação/Exportação:** Previsões baseadas em dados históricos.

### Privacidade e Segurança:  
1. **Proteção de Dados:**  
   - Criptografia de senhas e tokens JWT.  

2. **Controle de Acesso:**  
   - Autenticação JWT para proteger endpoints.

3. **Auditoria e Conformidade:**  
   - Monitoramento de logs e revisões de segurança.

### Arquitetura do Projeto:
1. **Autenticação:**  
   - Segurança através de tokens JWT para endpoints protegidos.  

2. **Ingestão de Dados:**  
   - Download dos dados CSV diretamente da Embrapa com scraping feito em **download.py**.  

3. **Processamento de Dados:**  
   - Armazenamento e limpeza dos arquivos CSV, além da geração de gráficos de análise no arquivo **app.py**.  

4. **Geração de "Dimensão País":**  
   - Função em **utils.py** que gera o arquivo consolidado com dados de importação e exportação.

5. **Machine Learning:**  
   - Treinamento de modelos preditivos com os dados CSV para análises futuras.

### Estrutura de Diretórios:
- `app.py`: Rotas HTTP, autenticação JWT e geração de gráficos.  
- `config.py`: Configurações globais.  
- `auth.py`: Funções de login e autenticação.  
- `download.py`: Download e visualização de arquivos CSV.  
- `utils.py`: Funções de suporte, como geração de "Dimensão País".  
- `templates/`: Páginas HTML.  
- `static/`: Gráficos gerados armazenados para o usuário.

### Deploy:
O deploy da aplicação será feito utilizando **Render**, com integração contínua (CI/CD). Cada nova versão da aplicação será implantada automaticamente no servidor, garantindo uma atualização frequente e segura para os usuários.

### Testes:
O teste dos endpoints será feito através do **Postman**, com a criação de cenários de login, download de arquivos e geração de gráficos. Testes automatizados serão implementados para garantir a robustez da aplicação.

---

Este README contém as informações necessárias para uso, implantação e manutenção da API Vitibrasil.
