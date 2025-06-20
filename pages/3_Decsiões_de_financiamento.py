import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.title("Empresas excessivamente confiantes por Ano e Setor ")
st.write("Análise usando a proxie oc3 (dívida / valor de mercado), que atua na dimensão das decisões de financiamento das organizações.")
st.write("divev_dif = nível de endividamento em relação à mediana dos setor.")

try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

if 'divev' not in df.columns or 'mediana_divev' not in df.columns:
    st.error("As colunas 'divev' e/ou 'mediana_divev' não estão presentes nos dados.")
    st.stop()

df['divev_dif'] = df['divev'] - df['mediana_divev']

variaveis_desempenho = ['wroa', 'wroaebit', 'wroe', 'wqtobin', 'wmgop', 'wopor', 'lnat', 'divbrat']
setores_disponiveis = sorted(df['setor'].dropna().unique())

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

df_filtrado = df[
    (df['setor'].isin(setores_filtrados)) &
    (df['ano'] == ano_selecionado) &
    (df['oc3'] == 1)
]

contagem_por_setor = df_filtrado.groupby('setor').size().reset_index(name='quantidade').sort_values('quantidade', ascending=False)

if contagem_por_setor.empty:
    st.warning("Não há dados para os filtros selecionados.")
else:
    fig = px.bar(
        contagem_por_setor,
        x='quantidade',
        y='setor',
        orientation='h',
        labels={'quantidade': 'Quantidade de Empresas', 'setor': 'Setor'},
        title=f"Empresas com OC3 = 1 no ano {ano_selecionado}",
        text='quantidade',
        template='plotly_white',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=40, t=50, b=40))
    st.plotly_chart(fig, use_container_width=True)

# Preparar top 10 maior excesso de confiança (decrescente)
top_10_maior_conf = df_filtrado.sort_values('divev_dif', ascending=False).head(10).copy()
top_10_maior_conf.insert(0, '#', range(1, len(top_10_maior_conf) + 1))

# Preparar top 10 menor excesso de confiança (crescente)
top_10_menor_conf = df_filtrado.sort_values('divev_dif', ascending=True).head(10).copy()
top_10_menor_conf.insert(0, '#', range(1, len(top_10_menor_conf) + 1))

col1, col2 = st.columns(2)

with col1:
    st.subheader("10 Empresas com maior nível de Excesso de Confiança Gerencial")
    st.dataframe(
        top_10_maior_conf[['#', 'ano', 'setor', 'ticker', 'divev_dif']].reset_index(drop=True),
        use_container_width=True
    )

with col2:
    st.subheader("10 Empresas com menor nível de Excesso de Confiança Gerencial")
    st.dataframe(
        top_10_menor_conf[['#', 'ano', 'setor', 'ticker', 'divev_dif']].reset_index(drop=True),
        use_container_width=True
    )

# Tabela completa com todos os dados filtrados e numeração iniciando em 1
colunas_exibir = ['ano', 'setor', 'ticker', 'oc3'] + variaveis_desempenho
df_exibir = df_filtrado[colunas_exibir].copy()
df_exibir.insert(0, '#', range(1, len(df_exibir) + 1))

st.subheader("📋 Dados Filtrados")
st.dataframe(df_exibir.reset_index(drop=True), use_container_width=True, height=600)

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_exibir.to_excel(writer, index=False, sheet_name='Empresas')

st.download_button(
    label="📥 Baixar dados em Excel",
    data=output.getvalue(),
    file_name="empresas_oc3_filtradas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
