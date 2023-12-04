import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup
import requests

clientes = pd.read_excel('./clientes.xlsx')
# REALIZANDO A REQUISIÇÃO DA PÁGINA E CONVERTENDO O CONTEÚDO EM OBJETO SOUP
page_request = requests.get('https://www.uol.com.br/esporte/futebol/campeonatos/brasileirao/')
soup_content = BeautifulSoup(page_request.content, 'html.parser')

# CRIANDO UM DICIONÁRIO PARA ARMEZAR OS DADOS COLETADOS
dictionaty_data ={
    'Classificação': [],
    'Equipe': []
}

# ENCONTRANDO ELEMENTO DA TABELA NO OBJETO SOUP
for line in soup_content.find('table', {'class': "data-table name"}).select('tbody > tr'):
    dictionaty_data['Classificação'].append(str(line.find('span', {'class': 'position'}).text.strip()))
    dictionaty_data['Equipe'].append(str(line.select_one('span.name > div > div:nth-of-type(1)').text.strip()))

# CRIANDO UM DATAFRAME PARA ARMAZENAR OS DADOS COLETADOS
dataframe = pd.DataFrame(dictionaty_data)

clientes = pd.read_excel('./clientes.xlsx')

for row in clientes.values:
    msg = MIMEMultipart()
    msg['Subject'] = 'Projeto Integrador 5 termo BigData:)'    
    msg['From'] = 'seu email'
    msg['To'] = row[1]
    message = f"OLá meu amigo {row[0]}, segue as informaçoes da Tabela do Brasileirão serie A:\n\n {dataframe.to_string(index=False)}"
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login('seu email', 'sua senha')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


