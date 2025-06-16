Este repositório apresenta um produto técnico desenvolvido a partir da dissertação de mestrado profissional em Administração no Instituto Federal de Minas Gerais – Campus Formiga.

A pesquisa, intitulada "EXCESSO DE CONFIANÇA GERENCIAL E DESEMPENHO FINANCEIRO: uma análise das empresas de capital aberto do Brasil", integra a linha de Finanças Comportamentais e Tomada de Decisão do Programa de Pós-Graduação em Administração.

A dissertação foi elaborada pela discente Letícia Carla Arruda Janacaro, como parte das exigências para obtenção do título de Mestre, sob orientação do Prof. Dr. Bruno César de Melo Moreira e coorientação do Prof. Dr. Lélis Pedro de Andrade.

A dissertação completa pode ser consultada no repositório de produções intelectuais do Mestrado Profissional em Administração do Instituto Federal de Minas Gerais – Campus Formiga, disponível em: https://www.formiga.ifmg.edu.br/mestrado-profissional-em-administracao/producoes-intelectuais.

**Aplicativo:** https://overconfidence.streamlit.app/ 

A partir deste repositório, um aplicativo interativo foi desenvolvido em Streamlit com o objetivo de facilitar a análise das informações relativas ao excesso de confiança gerencial e ao desempenho das empresas de capital aberto do Brasil, listadas na B3. Ele permite que os usuários explorem dados de forma dinâmica, visualizando relações entre variáveis, resíduos de regressões, indicadores de desempenho e níveis de governança corporativa.

A interface oferece filtros por ano, setor econômico e diferentes classificações de grupos, possibilitando análises segmentadas e detalhadas. Além disso, o aplicativo gera gráficos e visualizações que auxiliam na compreensão dos padrões de crescimento, desempenho e eficiência empresarial.

O aplicativo também promove a ciência aberta, disponibilizando a base de dados utilizada, permitindo que usuários realizem suas próprias análises, reproduzam os resultados ou desenvolvam pesquisas complementares.


#### 📊 Mensuração do Excesso de Confiança Gerencial e do Desempenho
As variáveis descritas no quadro abaixo representam proxies usadas para medir o **Excesso de Confiança Gerencial** em diferentes aspectos de decisões financeiras.


| Variável | Medida                                | Tipo                           | Método de Medição                                                                                                                                    |
|----------|----------------------------------------|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| oc1      | CAPEX                                  | Decisões de investimento       | Se os gastos de capital da empresa, quando escalados pelos ativos do ano anterior, excedem a mediana da indústria naquele ano (1); caso contrário, 0. |
| oc2      | Excesso de investimento                | Decisões de investimento       | Se o resíduo da regressão do crescimento total de ativos sobre o crescimento de vendas for maior que zero (1); caso contrário, 0.                   |
| oc3      | Dívida / Valor de mercado da empresa   | Decisões de financiamento      | A soma da dívida de longo e curto prazo dividida pelo valor de mercado da empresa. Assume 1 se superar a mediana anual da indústria, e 0 caso contrário. |
| oc4      | DIVYLD (Rendimento de dividendos)      | Decisões de financiamento      | O rendimento de dividendos é igual aos dividendos por ação dividido pelo preço da ação. Assume 1 se o rendimento for zero, e 0 caso contrário.      |
| oc134    | *                                      | Decisões de investimento e financiamento | Índice composto pelas proxies oc1, oc3 e oc4.                                                                                                   |
| oc234    | *                                      | Decisões de investimento e financiamento | Índice composto pelas proxies oc2, oc3 e oc4.                                                                                                   |


As variáveis listadas a seguir representam diferentes indicadores financeiros utilizados para avaliar o **desempenho** das empresas.

| Variável          | Descrição                                                                                                         |
|-------------------|-------------------------------------------------------------------------------------------------------------------|
| Q de Tobin        | A soma do valor de mercado das ações e do valor de mercado das dívidas, dividido pelo valor de reposição dos ativos, no final do ano t. |
| ROE               | O lucro líquido dividido pelo patrimônio líquido, no final do ano t.                                              |
| ROA               | Desempenho da empresa medido pelo retorno sobre ativos, no final do ano t.                                        |
| ROAEBIT           | Retorno sobre ativos antes de juros e impostos, calculado como lucro operacional dividido pelos ativos totais, no final do ano t. |
| Margem Operacional| Lucro operacional dividido pelas vendas.                                                                          |

#### ✅ Finalidades dos itens do repositório:
.devcontainer/: Armazena arquivos de configuração para ambientes de desenvolvimento em containers (ex.: GitHub Codespaces ou VSCode Dev Containers).

pages/: Contém os scripts Python que representam as diferentes páginas do aplicativo Streamlit.

README.md: Documento de apresentação do projeto, com informações sobre o objetivo, instalação, uso e detalhes importantes.

dados.xlsx: Arquivo com a base de dados utilizada pelo aplicativo, disponibilizado para download. Pode ser utilizado livremente pelos usuários para realizar análises, replicar os resultados ou desenvolver novas pesquisas, promovendo a ciência aberta.

home.py: Script responsável por definir a página inicial do app no Streamlit, servindo como ponto de entrada para os usuários.

requirements.txt: Arquivo que lista todas as bibliotecas e dependências necessárias para rodar o projeto Python.
