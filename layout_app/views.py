from django.shortcuts import render

import pandas as pd
from tqdm import tqdm
from json import dump, dumps


def lista_de_servicos():
    df = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Composicoes')
    filtro = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Lista')
    # filtro = filtro[(filtro['FONTE'] == 'SINAPI')]

    sinapi = pd.DataFrame({
        # 'FONTE': [],
        'CODIGO DA COMPOSICAO': [],
        'DESCRICAO DA COMPOSICAO': [],
        'UNIDADE': [],
        'CUSTO TOTAL': [],
        'TIPO ITEM': [],
        'FONTE ITEM': [],
        'CODIGO ITEM': [],
        'DESCRIÇÃO ITEM': [],
        'UNIDADE ITEM': [],
        'COEFICIENTE': [],
        'PRECO UNITARIO': [],
        'CUSTO TOTAL ITEM': [],
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


def carregar_composicao():
    composicoes = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Composicoes')
    try:
        composicoes = composicoes.drop(['DESCRICAO DA CLASSE', 'SIGLA DA CLASSE',
                                        'DESCRICAO DO TIPO 1', 'SIGLA DO TIPO 1', 'CODIGO DO AGRUPADOR',
                                        'DESCRICAO DO AGRUPADOR', 'ORIGEM DE PREÇO', 'ORIGEM DE PREÇO ITEM',
                                        '% ATRIBUÍDO SÃO PAULO', 'CUSTO MAO DE OBRA', '% MAO DE OBRA', 'CUSTO MATERIAL',
                                        '% MATERIAL','CUSTO EQUIPAMENTO', '% EQUIPAMENTO', 'CUSTO SERVICOS TERCEIROS',
                                        '% SERVICOS TERCEIROS', 'CUSTO OUTROS', '% OUTROS', 'VINCULO'], axis=1)
    except:
        pass

    serv = composicoes.drop_duplicates('CODIGO DA COMPOSICAO')
    serv = serv.drop(['TIPO ITEM', 'CODIGO ITEM', 'DESCRIÇÃO ITEM', 'UNIDADE ITEM',
                      'COEFICIENTE', 'PRECO UNITARIO', 'CUSTO TOTAL ITEM'], axis=1)

    composicao_all = []
    for c in serv.to_dict('records'):
        comp = composicoes[composicoes['CODIGO DA COMPOSICAO'] == c['CODIGO DA COMPOSICAO']]
        comp = comp.drop(['CODIGO DA COMPOSICAO', 'DESCRICAO DA COMPOSICAO', 'UNIDADE', 'CUSTO TOTAL'], axis=1)
        c['ITENS'] = comp.to_dict('records')
        composicao_all.append(c)

    # return composicoes.to_dict('records')
    return composicao_all


def decomposicao_insumos(lista_servicos):
    pass


def decomposicao(itens_orcamento, lista_insumos=None, lista_tratamento=None):
    li =
    if lista_insumos is None:
        lista_insumos = decomposicao_insumos(lista_servicos)


    if lista_tratamento is None:
        lista_tratamento = None

    if lista_tratamento:
        pass


def decomposicao_sintetica():
    composicao_all = carregar_composicao()
    lista_excel = pd.read_excel('D:/Projetos/LayoutCPU/LayoutCPU/static/proposta_inga_cheia.xlsx', sheet_name='Lista')
    lista = lista_excel['CODIGO'].to_list()

    for _ in range(10):
        selecao = []
        lista_sel = []
        for item in lista:
            for composicao in composicao_all:
                if (composicao['CODIGO DA COMPOSICAO']) == item:
                    selecao.append(composicao)
                    lista_sel.append(item)

        lista_composicoes = []
        for comp in selecao:
            for item in comp['ITENS']:
                if item['TIPO ITEM'] == 'COMPOSICAO':
                    lista_composicoes.append(item['CODIGO ITEM'])

        lista = set(set(lista_composicoes) | set(lista_sel))

        print(f'Composições: {len(composicao_all)}',
              f'Lista: {len(lista)}',
              f'Selecao: {len(selecao)}',
              f'Lista Seleção: {len(lista_sel)}'
              )

    # with open('D:/Projetos/json/selecao.json', 'w', encoding='UTF-8') as arq:
    #     dump(selecao, arq, indent=4, ensure_ascii=False, separators=(',', ': '))
    #
    # orcamento = composicoes.loc[composicoes['CODIGO DA COMPOSICAO'].isin(lista)]
    #
    # orcamento.to_excel('D:/Projetos/json/orcamento.xlsx')

    return selecao