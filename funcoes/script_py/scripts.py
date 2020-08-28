import time
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from json import load, loads, dump, dumps
from decimal import Decimal
from tqdm import tqdm

from conlicita_app.models import Licitacao
from conlicita_app.models import Empresa


option = Options()
option.headless = True
driver = webdriver.Chrome(options=option)


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


def abrir_json(arquivo):
    with open(arquivo, 'r', encoding='UTF-8') as file_data:
        data = load(file_data)
    return data


def raspar_dados_licitacao():
    acompanhamento = []
    formato = 'json'

    print('Fazendo Login na Pagina')
    login_conlicitacao()

    # todo modificar esse código para passar uma lista de licitações.
    print('Puxando Lista de Licitações')
    with open('./funcoes/json/acompanhar_licitacoes.json', 'r', encoding='UTF-8') as file_data:
        data = file_data.readlines()
        data = [loads(d) for d in data]

    print('Carregando os Arquivos')
    for i in tqdm(data[0], total=len(data[0])):
        num_conlicitacao = i
        url = f'https://consultaonline.conlicitacao.com.br/biddings/{num_conlicitacao}.{formato}'
        driver.get(url)
        element = driver.find_element_by_tag_name('pre')
        html_content = element.text.replace('\\n', ' ').replace('\\r', ' ')
        dados = loads(html_content)
        # time.sleep(2)
        acompanhamento.append(dados)

    driver.quit()

    with open('./funcoes/json/Acompanhamento.json', 'w', encoding='UTF-8') as file_data:
        dump(acompanhamento, file_data, indent=4, ensure_ascii=False, separators=(',', ': '))

    return acompanhamento


def importar_licitacoes():
    arquivo = './funcoes/json/Acompanhamento.json'
    certames = abrir_json(arquivo)

    for certame in certames:
        Licitacao(
            id_conlicitacao=certame['id'],
            orgao_uasg=certame['orgao_uasg'],
            orgao_endereco=certame['orgao_endereco'],
            orgao_cidade=certame['orgao_cidade'],
            orgao_estado=certame['orgao_estado'],
            orgao_cep=certame['orgao_cep'],
            edital=certame['edital'],
            edital_site=certame['edital_site'],
            edital_homepage=certame['edital_homepage1'],
            edital_homepage2=certame['edital_homepage2'],
            edital_preco=certame['edital_preco'],
            edital_tem=certame['edital_tem'],
            edital_status_id=certame['edital_status_id'],
            email=certame['email'],
            processo=certame['processo'],
            valor_estimado=certame['valor_estimado'],
            itens=certame['itens'],
            datahora_prazo=certame['datahora_prazo'],
            datahora_abertura=certame['datahora_abertura'],
            datahora_retirada=certame['datahora_retirada'],
            datahora_visita=certame['datahora_visita'],
            datahora_documento=certame['datahora_documento'],
            data_validade=certame['data_validade'],
            objeto=certame['objeto'],
            observacao=certame['observacao'],
            modified=certame['modified'],
            created=certame['created'],
            bidding_id=certame['bidding_id'],
            has_electronic_trading=certame['has_electronic_trading'],
            public_body=certame['public_body']['nome'],
            modality=certame['modality']['nome']
        ).save()


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


def raspar_dados_empresas():
    empresas = {}
    print('Abrindo Base de Concorrentes')
    concorrentes = pd.read_json('./funcoes/json/concorrentes.json')

    print('Fazendo Login no portal')
    login_conlicitacao()

    print('Acessando pagina de pesquisa')
    driver.get('https://consultaonline.conlicitacao.com.br/concorrentes')

    for c in range(len(concorrentes[0])):
        empresas[concorrentes[0][c]] = buscar_concorrente(concorrentes[0][c])
        print(f'Concorrente {concorrentes[0][c]} Coletado com Sucesso!')

    print('Gravando no Arquivo')
    with open('./funcoes/json/Empresas.json', 'w', encoding='UTF-8') as jp:
        js = dumps(empresas, indent=4, ensure_ascii=False)
        jp.write(js)

    driver.quit()

    return empresas


def importar_empresas():
    arquivo = './funcoes/json/Empresas.json'
    file_data = abrir_json(arquivo=arquivo)

    for key in list(file_data.keys()):
        Empresa(
            razao_social=file_data[key]['Razão Social'],
            cnpj=file_data[key]['CNPJ'].replace('.','').replace('/','').replace('-',''),
            endereco=file_data[key]['Endereço'],
            cidade=file_data[key]['Cidade'],
            estado=file_data[key]['Estado'],
            telefone=file_data[key]['Telefone'],
            email=file_data[key]['E-Mail'],
            situacao=file_data[key]['Situação'],
            tipo=file_data[key]['Tipo'],
            natureza=file_data[key]['Natureza'],
            abertura=datetime.strptime(file_data[key]['Abertura'], '%d/%m/%Y').date(),
            capital_social=Decimal(
                file_data[key]['Capital Social'].replace('R$', '').replace('.','').replace(',','.')
            ),
            segmento=file_data[key]['Segmentos'],
        ).save()
