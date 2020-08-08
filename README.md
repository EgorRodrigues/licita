# Licita
### Gestor de Licitações

O objetivo desse repositório é através do Django e Python organizar uma lista de Licitações e gerenciar cada uma de acordo com o interresse de participação da Empresa

* Cada empresa tera uma lista de licitações previamente selecionada do site https://conlicitacao.com.br/
essas licitaçõe serão cadastradas no banco de dados para avaliação

* Cada licitação devera possuir um campo para fazer uploads dos arquivos da licitação (Edital e Anexos)

* Cada Licitação terá dois Campos de Observação, um concernente a Habilitação e o Outro a Proposta

* Cada observação terá um checkbox do tipo Null, True e False

* Ao final uma caixa de seleção de status, que poderá ser gerenciada por botões, que informarão se a licitação foi Descartada, Aprovada (para Participar) ou em Obsevação

* A listagem de licitação devará possuir filtros por data, preço e status

* 

#### 1º Passo:

Capturar as informações das licitações e criar um Json para porteriomente popular o banco de dados e 

#### 2º Passo:

* Criar os models para armazenar as informações, e organizar as empresas
