import streamlit as st

# ====== Estilo CSS personalizado ======
st.markdown("""
    <style>
        body, .css-18e3th9, .main {
            background: linear-gradient(135deg, #f0f4f8, #d9e2ec) !important;
            min-height: 100vh;
        }
        /* Mantém o texto e fonte */
        .main, body {
            color: #1F2937;
            font-family: 'Inter', sans-serif;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        h2, h4 {
            color: #1E3A8A;
        }
        a {
            color: #2563EB;
            text-decoration: none;
            transition: color 0.2s;
        }
        a:hover {
            color: #1E40AF;
            text-decoration: underline;
        }
        hr {
            border: none;
            height: 2px;
            background-color: #1E3A8A;
            margin: 20px 0;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #d1d5db;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #1E3A8A;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ====== Cabeçalho ======
st.markdown("""
     <h2 style="text-align: center;">EXCESSO DE CONFIANÇA GERENCIAL E DESEMPENHO</h2>
     <h4 style="text-align: center;">Uma análise das empresas de capital aberto do Brasil</h4>
""", unsafe_allow_html=True)

# ====== Conteúdo organizado em abas ======
tab1, tab2, tab3, tab4 = st.tabs(["Aplicativo", "Conceito", "Métricas", "Dados"])

with tab1:
    st.markdown("""
        <div class="card">
            <h4>📚 Sobre o aplicativo</h4>
            <p style='text-align: justify;'>
                Este aplicativo apresenta um produto técnico desenvolvido a partir da dissertação de mestrado profissional em Administração no Instituto Federal de Minas Gerais – Campus Formiga.<br><br>
                A pesquisa, intitulada <strong>"EXCESSO DE CONFIANÇA GERENCIAL E DESEMPENHO FINANCEIRO: uma análise das empresas de capital aberto do Brasil"</strong>, integra a linha de Finanças Comportamentais e Tomada de Decisão do Programa de Pós-Graduação em Administração.<br><br>
                A dissertação foi elaborada pela discente Letícia Carla Arruda Janacaro, como parte das exigências para obtenção do título de Mestre, sob orientação do Prof. Dr. Bruno César de Melo Moreira e coorientação do Prof. Dr. Lélis Pedro de Andrade.<br><br>
                🔗 <a href="https://www.formiga.ifmg.edu.br/mestrado-profissional-em-administracao/producoes-intelectuais" target="_blank">Acesse a dissertação completa no repositório do IFMG</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
        <div class="card">
            <h4> 📝 Conceito: Excesso de Confiança Gerencial</h4>
            <p style='text-align: justify;'>
                O excesso de confiança gerencial ocorre no contexto corporativo e é caracterizado pela manifestação da superestimação, superposição ou excesso de precisão, conforme previsto e aceito pela literatura da área (Malmendier & Tate, 2005b; Moore & Healy, 2008; M. Zavertiaeva et al., 2018), adicionando o locus gerencial de interação. Para a formulação deste conceito, assume-se que as decisões organizacionais podem ser tomadas por diferentes gestores, em diferentes níveis hierárquicos e potencialmente construída por diversos atores. Devido a inespecificidade do tomador de decisão, ao contrário do que ocorre com o excesso de confiança do CEO, e à diversidade potencial de tomadores de decisão, as decisões refletem melhor as características da empresa. Essas características são sinalizadas por sua gestão, conjunto de gestores, independentemente de seus níveis hierárquicos, que figura incluindo os aspectos endógenos aos indivíduos, como o viés, e aspectos exógenos, como a cultura corporativa e as regras de confiança, esta última, conforme relatado por (Cheng et al., 2021).
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
        <div class="card">
        <h4>📊 Mensuração do Excesso de Confiança Gerencial</h4>
        <p>As variáveis abaixo representam proxies usadas para medir o <strong>Excesso de Confiança Gerencial</strong>:</p>
        <table>
            <tr>
                <th>Variável</th>
                <th>Medida</th>
                <th>Tipo</th>
                <th>Método de Medição</th>
            </tr>
            <tr>
                <td>oc1</td>
                <td>CAPEX</td>
                <td>Decisões de investimento</td>
                <td>Se os gastos de capital da empresa, escalados pelos ativos do ano anterior, excedem a mediana da indústria (1); caso contrário, 0.</td>
            </tr>
            <tr>
                <td>oc2</td>
                <td>Excesso de investimento</td>
                <td>Decisões de investimento</td>
                <td>Se o resíduo da regressão do crescimento total de ativos sobre o crescimento de vendas for maior que zero (1); caso contrário, 0.</td>
            </tr>
            <tr>
                <td>oc3</td>
                <td>Dívida / Valor de mercado</td>
                <td>Decisões de financiamento</td>
                <td>Soma da dívida de longo e curto prazo dividido pelo valor de mercado. Assume 1 se superar a mediana da indústria; caso contrário, 0.</td>
            </tr>
            <tr>
                <td>oc4</td>
                <td>DIVYLD (Rendimento de dividendos)</td>
                <td>Decisões de financiamento</td>
                <td>Rendimento de dividendos igual aos dividendos por ação dividido pelo preço da ação. Assume 1 se for zero; caso contrário, 0.</td>
            </tr>
            <tr>
                <td>oc134</td>
                <td>*</td>
                <td>Investimento e financiamento</td>
                <td>Índice composto pelas proxies oc1, oc3 e oc4.</td>
            </tr>
            <tr>
                <td>oc234</td>
                <td>*</td>
                <td>Investimento e financiamento</td>
                <td>Índice composto pelas proxies oc2, oc3 e oc4.</td>
            </tr>
        </table>
    """ , unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4>💼 Indicadores de Desempenho</h4>
        <p>As variáveis listadas a seguir representam diferentes indicadores financeiros utilizados para avaliar o <strong>desempenho</strong> das empresas:</p>
        <table>
            <tr>
                <th>Variável</th>
                <th>Descrição</th>
            </tr>
            <tr>
                <td>Q de Tobin</td>
                <td>Valor de mercado das ações + dívidas dividido pelo valor de reposição dos ativos.</td>
            </tr>
            <tr>
                <td>ROE</td>
                <td>Lucro líquido dividido pelo patrimônio líquido.</td>
            </tr>
            <tr>
                <td>ROA</td>
                <td>Retorno sobre ativos no final do ano t.</td>
            </tr>
            <tr>
                <td>ROAEBIT</td>
                <td>Retorno sobre ativos antes de juros e impostos.</td>
            </tr>
            <tr>
                <td>Margem Operacional</td>
                <td>Lucro operacional dividido pelas vendas.</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
        <div class="card">
            <h4>📥 Acesso aos dados e repositório</h4>
            <p>Para acessar o repositório no GitHub ou baixar os dados completos, clique no link abaixo:</p>
            🔗 <a href="https://github.com/leticiaarrudaedu/overconfidence" target="_blank">Repositório no GitHub</a>
        </div>
    """, unsafe_allow_html=True)
