import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from json import loads, dump


driver = webdriver.Chrome()
formato = 'json'

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

print('Fazendo Login na Pagina')
login_conlicitacao()

print('Abrindo Lita de Licitações para Acompanhamento')
with open('../json/acompanhar_licitacoes.json', 'r', encoding='UTF-8') as file_data:
    data = file_data.readlines()
    data = [loads(d) for d in data]

acompanhamento = []

for i in data[0]:
    print(i)
    num_conlicitacao = i
    url = f'https://consultaonline.conlicitacao.com.br/biddings/{num_conlicitacao}.{formato}'
    driver.get(url)
    element = driver.find_element_by_tag_name('pre')
    html_content = element.text.replace('\\n', ' ').replace('\\r', ' ')
    dados = loads(html_content)
    time.sleep(2)
    acompanhamento.append(dados)

with open('../json/Acompanhamento.json', 'w', encoding='UTF-8') as file_data:
    dump(acompanhamento, file_data, indent=4,  ensure_ascii=False, separators=(',', ': '))

driver.quit()
