import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Excesso de Confiança Gerencial", layout="wide")

st.title("Empresas Excessivamente Confiantes por Ano e Setor")
st.write("Análise usando a proxy OC3 (dívida / valor de mercado), que atua na dimensão das decisões de financiamento das organizações.")

# --- Importando os dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# --- Verificando colunas necessárias
if 'divev' not in df.columns or 'mediana_divev' not in df.columns:
    st.error("As colunas 'divev' e/ou 'mediana_divev' não estão presentes nos dados.")
    st.stop()

# --- Calculando diferença de divev
df['divev_dif'] = df['divev'] - df['mediana_divev']

# --- Variáveis
variaveis_desempenho = ['wroa', 'wroaebit', 'wroe', 'wqtobin', 'wmgop', 'wopor', 'lnat', 'divbrat']
setores_disponiveis = sorted(df['setor'].dropna().unique())

# --- Filtros
setores_selecionados = st.multiselect(
    "Selecione os setores:",
    options=['Selecionar todos'] + setores_disponiveis,
    default=['Selecionar todos']
)

if 'Selecionar todos' in setores_selecionados:
    setores_filtrados = setores_disponiveis
else:
    setores_filtrados = setores_selecionados

if not setores_filtrados:
    st.warning("Selecione pelo menos um setor.")
    st.stop()

anos_disponiveis = sorted(df[df['setor'].isin(setores_filtrados)]['ano'].dropna().unique())
ano_selecionado = st.selectbox("Selecione o ano:", options=anos_disponiveis)

# --- Filtrando os dados
df_filtrado = df[
    (df['setor'].isin(setores_filtrados)) &
    (df['ano'] == ano_selecionado) &
    (df['oc3'] == 1)
]

# --- Contagem por setor
contagem_por_setor = df_filtrado.groupby('setor').size().reset_index(name='quantidade').sort_values('quantidade', ascending=False)

# --- Cards de Resumo
st.subheader("Resumo dos Dados Selecionados")

col1, col2, col3 = st.columns(3)

col1.metric("Ano Selecionado", f"{ano_selecionado}")
col2.metric("Setores Selecionados", f"{len(setores_filtrados)}")
col3.metric("Empresas OC3 = 1", f"{df_filtrado['ticker'].nunique()}")

st.divider()

# --- Gráfico
if contagem_por_setor.empty:
    st.warning("Não há dados para os filtros selecionados.")
else:
    st.subheader(f"Distribuição das Empresas com OC3 = 1 no Ano {ano_selecionado}")
    
    fig = px.bar(
        contagem_por_setor,
        x='quantidade',
        y='setor',
        orientation='h',
        labels={'quantidade': 'Quantidade de Empresas', 'setor': 'Setor'},
        text='quantidade',
        template='plotly_white',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=150, r=40, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Top 10 Empresas
top_10_maior_conf = df_filtrado.sort_values('divev_dif', ascending=False).head(10)
top_10_menor_conf = df_filtrado.sort_values('divev_dif', ascending=True).head(10)

col1, col2 = st.columns(2)

with col1:
    st.subheader("10 Empresas com Maior Nível de Excesso de Confiança")
    st.dataframe(
        top_10_maior_conf[['ano', 'setor', 'ticker', 'divev_dif']].reset_index(drop=True),
        use_container_width=True
    )

with col2:
    st.subheader("10 Empresas com Menor Nível de Excesso de Confiança")
    st.dataframe(
        top_10_menor_conf[['ano', 'setor', 'ticker', 'divev_dif']].reset_index(drop=True),
        use_container_width=True
    )

st.divider()

# --- Dados Filtrados
st.subheader("Dados Filtrados")

colunas_exibir = ['ano', 'setor', 'ticker', 'oc3'] + variaveis_desempenho
df_exibir = df_filtrado[colunas_exibir].copy()

st.dataframe(
    df_exibir.reset_index(drop=True),
    use_container_width=True
)

# --- Download dos Dados
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_exibir.to_excel(writer, index=False, sheet_name='Empresas')

st.download_button(
    label="Baixar Dados em Excel",
    data=output.getvalue(),
    file_name="empresas_oc3_filtradas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
