# Aplicação de raspagem de dados

Esta aplicação usa Selenium e BeautifulSoup para raspar dados de uma tabela em um site e exportá-los para uma planilha do Excel.
O site em questão é o [Portal da Transparência](https://www.portaldatransparencia.gov.br/), que contém informações sobre os gastos públicos do governo federal.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: `selenium`, `beautifulsoup4`, `pandas`

## Instalação

1. Clone o repositório ou faça o download do código-fonte.
2. Crie um ambiente virtual usando o comando `python -m venv venv`.
3. Ative o ambiente virtual usando o comando `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/MacOS).
4. Instale as dependências usando o comando `pip install -r requirements.txt`.

## Uso

1. Execute o script usando o comando `python app.py`.
2. Os dados raspados serão salvos em um arquivo chamado `dados.xlsx` na mesma pasta do script.

## Licença

## Possíveis problemas
O projeto usa o driver do Chrome para o Selenium. Se você estiver usando outro navegador, você precisará baixar o driver correspondente e substituir o arquivo `chromedriver.exe` na pasta `drivers`.
O tempo de espera para a página carregar pode ser alterado na linha 13 do arquivo `app.py`.
O tempo de raspagem pode variar de acordo com a velocidade da sua conexão com a internet.
O site pode mudar a estrutura da tabela, o que pode causar problemas na raspagem dos dados.
Mudanças na estrutura da tabela podem causar problemas na raspagem dos dados.
A raspagem dos dados pode ser feita de várias formas, mas a escolhida para este projeto foi a mais simples e direta.

Achei o tempo de raspagem muito longo. Como posso melhorar isso?

Este projeto está licenciado sob a licença MIT.