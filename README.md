# Licita
### Gestor de Licitações

O objetivo desse repositório é através do Django e Python organizar uma lista de Licitações e gerenciar cada uma de acordo com o interresse de participação da Empresa

* Cada empresa tera uma lista de licitações previamente selecionada do site https://conlicitacao.com.br/
essas licitaçõe serão cadastradas no banco de dados para avaliação

* Cada licitação devera possuir um campo para fazer uploads dos arquivos da licitação (Edital e Anexos)

* Cada Licitação terá dois Campos de Observação, um concernente a Habilitação e o Outro a Proposta

* Ao final uma caixa de seleção de status, que poderá ser gerenciada por botões, que informarão se a licitação foi Descartada, Aprovada (para Participar) ou em Obsevação, e o default será Não Avaliado

* A listagem de licitação devará possuir filtros por data, preço e status

* Criar 5 listagens de licitações de acordo com o seu status:
    * Listagem completa das licitações;
    * Listagem das Licitações Selecionadas (Escolhidas para Analise mais detalhada);
    * Listagem das licitações descartadas ( Licitações que em uma fase anterior foram Selecionadas);
    * Listagem das licitações p/ Acompanhamento (são as licitações que foram descartadas, porem há o interrese de acompanhar as proximas etapas);
    * Listagem das licitações que irão participar (Licitações escolhidas e aprovadas para participação, nessas haverá compos para upload de documentos de participação)
    

#### 1º Passo:

* Capturar as informações das licitações e criar um Json para porteriomente popular o banco de dados e 

#### 2º Passo:

* Criar os models para armazenar as informações, e organizar as empresas

### 3º Passo:

* Criar o relacinamento entre as empresas e as licitações, e criar o painel de configuração das licitações.