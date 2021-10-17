# Análise das causas do aumento do desmatamento na Amazônia em 2019

Este trabalho visa analisar a relação dos incrementos de desmatamento na Amazônia, medidos pelo projeto Prodes do INPE,
com outras variáveis, com o objetivo de identificar as causas para o aumento do desmatamento.

**Estágio atual da análise:** Por hora, analisamos apenas a relação entre desmatamento e o orçamento federal dedicado à preservação do meio ambiente.


## Estrutura do projeto:

    .
    ├── README.md         <- Este documento
    ├── requirements.txt  <- Pacotes de python necessários para este projeto
    ├── dados             <- Diretório onde salvar os dados
    ├── analises          <- Diretório com as análises feitas (notebooks de python)
    └── resultados        <- Onde os gráficos serão salvos pelos notebooks
    

## Dados

As análises realizadas aqui utilizam aproximadamente 450 MB de dados. Com exceção de alguns arquivos criados por nós que agrupam ações orçamentárias, todos
os dados são públicos e estão disponíveis na internet. Para facilitar, disponibilizamos os dados já na estrutura e formato utilizados pelas análises.

Porém, como os dados são volumosos, eles não estão neste repositório, mas se encontram em um
[tarfile](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/orcamento_processado_MMA_SFB_2010-2021.zip)
comprimido (`.tar.gz`). Em princípio, basta baixá-lo e descomprimi-lo dentro do diretório `dados` para que as análises possam localizar
os arquivos necessários. A estrutura de sub-diretórios utilizada pelo projeto está guardada dentro do tarfile e deve ser reproduzida  após a descompressão.


## Conteúdo dos notebooks

O processamento, exploração e análise dos dados foram feitos com python em notebooks jupyter,
localizados na pasta `analises`.

### `exploracao_dados_prodes.ipynb`

Análise dos dados de desmatamento do Prodes de maneira individual. Os gráficos de desmatamento ao longo do tempo
e por estado foram produzidos aqui.

### `exploracao_do_orcamento_de_GLOs.ipynb`

Exploração do orçamento do governo com operações de garantia da lei e da ordem (GLOs), para descobrir como identificar as
GLOs ambientais. Este arquivo foi utilizado apenas para esse fim, não resultando em nenhum gráfico utilizado.

### `modelo_incremento-prodes_a-partir-do_deter.ipynb`

Aqui foi criado o modelo polinomial que relaciona os dados de avisos de desmatamento do Deter com os incrementos de
desmatamento do Prodes, com o objetivo de antecipar a medida do Prodes para 2021. Além disso, exploramos aqui os dados
do Deter. O gráfico para a relação entre dados do Deter e Prodes também foi criado aqui.

### `analise_orcamento_e_desmatamento.ipynb`

Aqui foi feita a análise e gráficos das evoluções do orçamento do MMA (com e sem GLOs), das superintendências do IBAMA e
explorações gerais dos dados de orçamento de despesa. Além disso, aqui nós analisamos a relação entre o orçamento o desmatamento,
ou seja: _este é o principal arquivo de análise sobre essa relação_.

## Contato

Quaisquer dúvidas a respeito deste trabalho podem ser encaminhadas a [Henrique Xavier](http://henriquexavier.net) (<https://github.com/hsxavier>).