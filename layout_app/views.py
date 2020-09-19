from django.shortcuts import render

import pandas as pd
from tqdm import tqdm

def lista_de_servicos():
    df = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Composicoes')
    filtro = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Lista')
    # filtro = filtro[(filtro['FONTE'] == 'SINAPI')]

    sinapi = pd.DataFrame({
        # 'FONTE': [],
        'CODIGO DA COMPOSICAO': [],
        'DESCRICAO DA COMPOSICAO':[],
        'UNIDADE':[],
        'CUSTO TOTAL':[],
        'TIPO ITEM': [],
        'FONTE ITEM': [],
        'CODIGO ITEM': [],
        'DESCRIÇÃO ITEM': [],
        'UNIDADE ITEM': [],
        'COEFICIENTE': [],
        'PRECO UNITARIO': [],
        'CUSTO TOTAL ITEM':[],
        })
    for index, row in tqdm(filtro.iterrows(), total=len(filtro)):
        codigo = row['CODIGO']
        composicao = df[(df['CODIGO DA COMPOSICAO'] == codigo)]
        sinapi = pd.concat([sinapi, composicao])
    return sinapi


def budgets(request):
    lista = lista_de_servicos()
    dadosUnicos = lista['CODIGO DA COMPOSICAO'].drop_duplicates()
    composicoes = []

    for index, row in dadosUnicos.iteritems():
        df_lista = lista[(lista['CODIGO DA COMPOSICAO'] == row)]
        servico = df_lista.iloc[0]
        itens = []
        for index, newrow in df_lista.iterrows():
            if str(newrow['CODIGO ITEM']) != 'nan':
                itens.append(
                    {
                        'codigo_item': newrow['CODIGO ITEM'],
                        'tipo_item': newrow['TIPO ITEM'],
                        'descricao_item': newrow['DESCRIÇÃO ITEM'],
                        'unidade_item': newrow['UNIDADE ITEM'],
                        'quantidade_item': newrow['COEFICIENTE'],
                        'preco_unitario_item': newrow['PRECO UNITARIO'],
                        'preco_total_item': newrow['CUSTO TOTAL ITEM']
                    }
                )

        composicoes.append({
            # 'fonte': servico['FONTE'],
            'codigo': servico['CODIGO DA COMPOSICAO'],
            'descricao': servico['DESCRICAO DA COMPOSICAO'],
            'unidade': servico['UNIDADE'],
            'itens': itens,
            'custo_total': servico['CUSTO TOTAL'],
            'mao_de_obra': servico['CUSTO MAO DE OBRA'],
            'material': servico['CUSTO MATERIAL'],
            'equipamento': servico['CUSTO EQUIPAMENTO'],
            # 'serv_terceiro': servico['CUSTO SERVICOS TERCEIROS']
        })

    return render(request, 'layout_app/budgets.html', {'composicoes': composicoes})
