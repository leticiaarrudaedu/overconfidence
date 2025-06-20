import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Título
st.title("Empresas por Ano, Setor e OC3")
st.write("Análise usando apenas o tipo de OC: oc3")

# Carregamento dos dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# Criar a variável divev_dif = divev - mediana_divev
if 'divev' not in df.columns or 'mediana_divev' not in df.columns:
    st.error("As colunas 'divev' e/ou 'mediana_divev' não estão presentes nos dados.")
    st.stop()

df['divev_dif'] = df['divev'] - df['mediana_divev']

# Configurações
variaveis_desempenho = ['wroa', 'wroaebit', 'wroe', 'wqtobin', 'wmgop', 'wopor', 'lnat', 'divbrat']
setores_disponiveis = sorted(df['setor'].dropna().unique())

# Filtro setores com opção "Selecionar todos"
setores_selecionados = st.multiselect(
    "Selecione os setores:",
    options=['Selecionar todos'] + setores_disponiveis,
    default=['Selecionar todos']
)

# Se selecionou "Selecionar todos", considera todos os setores
if 'Selecionar todos' in setores_selecionados:
    setores_filtrados = setores_disponiveis
else:
    setores_filtrados = setores_selecionados

# Validação
if not setores_filtrados:
    st.warning("Selecione pelo menos um setor.")
    st.stop()

# Filtragem considerando apenas oc3
df_filtrado = df[df['setor'].isin(setores_filtrados) & (df['oc3'] == 1)]

# Agrupamento por ano
contagem_por_ano = df_filtrado.groupby('ano').size().reset_index(name='quantidade')
contagem_por_ano = contagem_por_ano.sort_values('ano', ascending=False)

# Gráfico moderno com Plotly
if contagem_por_ano.empty:
    st.warning("Não há dados para os filtros selecionados.")
else:
    fig = px.bar(
        contagem_por_ano,
        x='quantidade',
        y=contagem_por_ano['ano'].astype(str),
        orientation='h',
        labels={'quantidade': 'Quantidade de Empresas', 'ano': 'Ano'},
        title=f"Empresas com OC3 = 1 nos setores selecionados",
        text='quantidade',
        template='plotly_white',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=60, r=40, t=50, b=40))
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar top 10 empresas com maior e menor excesso de confiança lado a lado
    top_10_maior_conf = df_filtrado.sort_values('divev_dif', ascending=False).head(10)
    top_10_menor_conf = df_filtrado.sort_values('divev_dif', ascending=True).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("10 Empresas com Maior Excesso de Confiança (divev_dif)")
        st.dataframe(top_10_maior_conf[['ano', 'setor', 'ticker', 'divev_dif']], use_container_width=True)

    with col2:
        st.subheader("10 Empresas com Menor Excesso de Confiança (divev_dif)")
        st.dataframe(top_10_menor_conf[['ano', 'setor', 'ticker', 'divev_dif']], use_container_width=True)

    # Tabela com detalhes das empresas
    colunas_exibir = ['ano', 'setor', 'ticker', 'oc3'] + variaveis_desempenho
    df_exibir = df_filtrado[colunas_exibir].copy()

    st.subheader("Dados das Empresas Selecionadas")
    st.dataframe(df_exibir, use_container_width=True)

    # Exportar para Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exibir.to_excel(writer, index=False, sheet_name='Empresas')

    st.download_button(
        label="📥 Baixar dados em Excel",
        data=output.getvalue(),
        file_name="empresas_oc3_filtradas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
