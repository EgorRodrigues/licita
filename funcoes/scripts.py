from json import load

from conlicita_app.models import licitacao


def abrir_json():
    with open('./funcoes/json/Acompanhamento.json', 'r', encoding='UTF-8') as file_data:
        data = load(file_data)
    return data


def importar_licitacoes():
    certames = abrir_json()
    for certame in certames:
        licitacao(
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
        ).save()

