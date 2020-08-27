from datetime import datetime
from json import load
from decimal import Decimal

from conlicita_app.models import Licitacao
from conlicita_app.models import Empresa


def abrir_json(arquivo):
    with open(arquivo, 'r', encoding='UTF-8') as file_data:
        data = load(file_data)
    return data


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
