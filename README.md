# Análise das causas do aumento do desmatamento na Amazônia em 2019

Este trabalho visa analisar a relação dos incrementos de desmatamento na Amazônia, medidos pelo projeto Prodes do INPE,
com outras variáveis, com o objetivo de identificar as causas para o aumento do desmatamento. Num primeiro momento, analisamos
apenas a relação do desmatamento com o orçamento do Ministério do Meio Ambiente (MMA). Em seguida, incluímos outras variáveis
na análise: quantidade de chuvas na região amazônica, preço de commodities agropecuárias e número de servidores do IBAMA. Embora
não tenha sido incluído na nota técnica final, também analisamos a relação com o PIB brasileiro deflacionado.

## Estrutura do projeto:

    .
    ├── README.md                                     <- Este documento
    ├── requirements.txt                              <- Principais pacotes de python necessários
    ├── dados                                         <- Diretório onde salvar os dados
    |   ├── arquivos-de-dados_orcamento.txt           <- Lista de arquivos do tarfile 1
    |   └── arquivos-de-dados_modelo-multivariado.txt <- Lista de arquivos do tarfile 2   
    ├── analises                                      <- Análises feitas (notebooks de python)
    |   └── xavy                                      <- Pasta com códigos auxiliares
    └── resultados                                    <- Onde os gráficos serão salvos
    

## Notas técnicas finais

As notas técnicas resultantes das análises deste repositório encontram-se disponíveis nos links:

* [Amazônia: alocação orçamentária errática, ineficiência das políticas públicas e descontrole do desmatamento](http://dados.movimentoacredito.org/notas_tecnicas/Nota_Tecnica_Desmatamento_e_Orcamento.pdf); e

* [O que explica o aumento do o desmatamento na Amazônia?](http://dados.movimentoacredito.org/notas_tecnicas/Nota_Tecnica_O_que_explica_o_desmatamento.pdf)

## Pacotes necessários

Os pacotes de Python necessários para rodar os principais resultados desse projeto estão listados no
arquivo `requirements.txt`. Alguns outros pacotes são importados pelos notebooks mas em seções que não
fazem parte da análise finalizada (e.g. `tensorflow` e `shap`). Essas seções foram mantidas nos notebooks
apenas como forma de registro.

## Dados

As análises realizadas aqui utilizam aproximadamente 675 MB de dados (ignorando os 4,6 GB de dados meteorológicos, veja a sub-seção _Dados de chuvas_).
Com exceção de alguns arquivos criados por nós (e.g. que agrupam ações orçamentárias), todos
os dados são públicos e estão disponíveis na internet. Para facilitar, disponibilizamos os dados já na estrutura e formato utilizados pelas análises.

Porém, como os dados são volumosos, eles não estão neste repositório, mas se encontram nos arquivos comprimidos (`.tar.gz`)
[tarfile 1 (análise do orçamento)](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-desmatamento-orcamento.tar.gz)
e [tarfile 2 (análise multivariada)](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz).
Em princípio, basta baixá-los e descomprimi-los dentro do diretório `dados` para que as análises possam localizar
os arquivos necessários. A estrutura de sub-diretórios utilizada pelo projeto está guardada dentro do tarfile e deve ser reproduzida após a descompressão.

A análise sobre a relação entre desmatamento e orçamento apenas depende dos dados no
[tarfile 1](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-desmatamento-orcamento.tar.gz). Já a análise da combinação de
várias variáveis _também_ depende dos dados no [tarfile 2](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz).
Os arquivos `dados/arquivos-de-dados_orcamento.txt` e `dados/arquivos-de-dados_modelo-multivariado.txt` contém a lista de arquivos de cada tarfile,
na estrutura de diretórios planejada.


### Dados de chuvas (precipitação)

Os dados de precipitação foram obtidos do Instituto Nacional de Meteorologia (INMET): <https://portal.inmet.gov.br/dadoshistoricos>. Por se tratar de uma
grande quantidade de dados (4,6 GB), não incluímos os dados brutos aqui ou em um link. Apenas o dado processado, agregado por Ano Prodes para a média na
Amazônia Legal, é fornecido no [tarfile 2](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz).
Caso seja de seu interesse tratar os dados brutos, os dados comprimidos (`.zip`) de cada ano
devem ser baixados do INMET e salvos na pasta `dados/brutos/clima`, e em seguida descompactados de maneira que todos os seus arquivos fiquem dentro
de uma pasta localizada em `dados/brutos/clima` cujo nome é o ano em questão, e.g.: `dados/brutos/clima/2014/`, `dados/brutos/clima/2015/`, etc. 

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

### `processamento_de_dados_de_chuvas.ipynb`

Este notebook faz o processamento, limpeza e agregamento dos dados de precipitação, partindo de dados horários de precipitação por
estação meteorológica, incompletos, para chegar na precipitação média na Amazônia Legal em cada Ano Prodes. Os dados de entrada devem ser baixados
do [INMET](https://portal.inmet.gov.br/dadoshistoricos) e os dados de saída (que serão utilizados pelo notebook
`modelo_multivariado_desmatamento.ipynb`) já estão disponíveis no
[tarfile 2](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz).

### `servidores_ibama.ipynb`

Este arquivo analisa a evolução do número de servidores do IBAMA a partir de duas fontes: o
[Portal da Transparência](http://www.portaltransparencia.gov.br/download-de-dados/servidores) e do
[Painel Estatístico de Pessoal (PEP)](https://www.gov.br/economia/pt-br/acesso-a-informacao/servidores/servidores-publicos/painel-estatistico-de-pessoal).
Em seguida, ele compara os dois dados e os combina para cobrir o período de 2010 a 2021 da melhor forma possível. Alguns gráficos relacionados
ao número de servidores do IBAMA são produzidos aqui, e este notebook também gera o arquivo de input já processado sobre o número de
servidores do IBAMA, que é utilizado em `modelo_multivariado_desmatamento.ipynb`. Os dados produzidos já estão disponíveis no
[tarfile 2](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz). 

### `modelo_multivariado_desmatamento.ipynb`

Esse notebook combina a evolução temporal de várias variáveis (orçamento, precipitação, número de servidores e preços de commodities) para
criar e testar modelos preditivos para o incremento de desmatamento. Além disso, ele também pre-processa os dados de commodities. Este é o
notebook principal da análise multivariada do desmatamento. Os dados de input necessários estão nos arquivos
[tarfile 1](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-desmatamento-orcamento.tar.gz)
e [tarfile 2](https://storage.googleapis.com/gab-compartilhado-publico/desmatamento/dados-modelo-multivariado.tar.gz).

## Contato

Quaisquer dúvidas a respeito deste trabalho podem ser encaminhadas a [Henrique Xavier](http://henriquexavier.net) (<https://github.com/hsxavier>).