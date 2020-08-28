from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import datetime
from json import load, loads, dump
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
