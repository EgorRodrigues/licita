import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from json import dump, load
#import json
import time


licitacoes = []

print("Iniciando...")

num_conlicitacao = 12918851
formato = 'json'

url = 'https://tramita.tce.pb.gov.br/tramita/login.jsf?login_novo_mural_licitacoes_generico=1'
url2 = 'https://tramita.tce.pb.gov.br/tramita/pages/novoMuralDeLicitacoesGenerico.jsf'
url3 = 'https://tramita.tce.pb.gov.br/tramita/consultatramitacao?processo='
url4 = 'https://tramita.tce.pb.gov.br/tramita/consultatramitacao?documento='
url5 = f'https://consultaonline.conlicitacao.com.br/biddings/{num_conlicitacao}.{formato}'
url6 = f'https://consultaonline.conlicitacao.com.br/minhas_licitacoes/biddings/{num_conlicitacao}/comments.json'
url7 = f'https://consultaonline.conlicitacao.com.br/boletim_web/public/licitacoes/{num_conlicitacao}/arquivos/'

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)  # options=option

print('Acessando o Site')
driver.get(url)
driver.get(url2)

print('Abrindo Pagina de Licitações...')

time.sleep(2)

driver.find_element_by_xpath('//input[@value="Licitações Previstas"]').click()

def scrap_tce(local, ente):
    driver.find_element_by_xpath(f'//option[@value="{local}"]').click()
    driver.find_element_by_xpath('//input[@id="body:mainForm:findAction-commandButton"]').click()

    if driver.find_element_by_xpath('//span[@id="body:mainForm:listResults"]').text == 'Resultado: 0 resultados.':
        df_full = pd.DataFrame()
    else:
        element = driver.find_element_by_xpath('//table[@class="base-h-dataTable"]')
        html_content = element.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0].head(200)
        df_full['Edital'] = "NaN"
        df_full['Ente'] = ente

    print(f'O local {local} foi coletado com Sucesso!')

    return df_full.to_dict('records')


locais = pd.read_json('../json/locais.json')

for local in locais:
    licitacoes.extend(scrap_tce(local, locais[local][0]))
    # licitacoes[locais[local][0]] = scrap_tce(local)

driver.quit()

print('Copiando para Arquivo')

with open('../json/licitacoes.json', 'w', encoding='UTF-8') as file_data:
    dump(licitacoes, file_data, indent=4,  ensure_ascii=False, separators=(',', ': '))
    # js = json.dumps(licitacoes, indent=4, ensure_ascii=False)
    # jp.write(js)
