from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import json


option = Options()
option.headless = True
driver = webdriver.Firefox(options=option) #options=option)
empresas = {}


def login_conlicitacao():
    driver.get('https://consultaonline.conlicitacao.com.br/users/login')

    login = 'adalberto@centralsolo.com.br'
    senha = 'solo535353'

    btn_xpath = '//input[@name="commit"]'
    login_id = 'login'
    senha_id = 'senha'

    driver.find_element_by_id(login_id).send_keys(login)
    driver.find_element_by_id(senha_id).send_keys(senha)
    driver.find_element_by_xpath(btn_xpath).click()


print('Abrindo Base de Concorrentes')
concorrentes = pd.read_json('../json/concorrentes.json')

print('Fazendo Login no portal')
login_conlicitacao()
time.sleep(2)

print('Acessando pagina de pesquisa')
driver.get('https://consultaonline.conlicitacao.com.br/concorrentes')


def buscar_concorrente(concorrente):
    driver.find_element_by_id('cnpj').clear()
    driver.find_element_by_id('cnpj').send_keys(concorrente)
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    time.sleep(3)

    element = driver.find_element_by_xpath('//div[@class="row mb-3"][1]')
    element2 = driver.find_element_by_xpath('//div[@class="row mb-3"][6]')
    html_content = element.get_attribute('outerHTML')
    html_content2 = element2.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    soup2 = BeautifulSoup(html_content2, 'html.parser')
    table = soup.find()
    table2 = soup2.find('table')
    t1 = table.find_all('dl')
    t2 = pd.read_html(str(table2))[0].to_dict('records')

    empresa = {}
    for n in range(len(t1)):
        if n == 13:
            empresa[t1[n - 1].find('dt').text] = list()
            for s in range(len(t1[n - 1].find_all('p'))):
                empresa[t1[n - 1].find('dt').text].append(t1[n - 1].find_all('p')[s].text)
        else:
            empresa[t1[n - 1].find('dt').text] = t1[n - 1].find('dd').text
    empresa['Licitacoes'] = t2

    return empresa


for c in range(len(concorrentes[0])):
    empresas[concorrentes[0][c]] = buscar_concorrente(concorrentes[0][c])
    print(f'Concorrente {concorrentes[0][c]} Coletado com Sucesso!')

print('Gravando no Arquivo')
with open('../json/Empresas.json', 'w', encoding='UTF-8') as jp:
    js = json.dumps(empresas, indent=4, ensure_ascii=False)
    jp.write(js)
