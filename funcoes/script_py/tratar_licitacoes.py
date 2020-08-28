import pandas as pd


def tratar():
    licitacoes = pd.read_json('./json/licitacoes.json', encoding='UTF-8', orient='')
    return licitacoes.to_dict()


if __name__ == '__main__':
    print(tratar())
