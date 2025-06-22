import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

# Título
st.title("Empresas por Nível de Governança Corporativa, Ano e Excesso de Confiança Gerencial")

# Carregamento dos dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# Garantir nomes em minúsculo para evitar erros
df.columns = df.columns.str.lower()

# Definir colunas de governança e de excesso de confiança
niveis_governanca = ['n1', 'n2', 'nm']
variaveis_oc = ['oc1', 'oc2', 'oc3', 'oc4', 'oc134', 'oc234']

# Anos disponíveis
anos_disponiveis = sorted(df['ano'].dropna().unique())

# Filtros interativos
st.sidebar.header("Filtros")

niveis_selecionados = st.sidebar.multiselect(
    "Selecione os níveis de governança:", niveis_governanca
)

anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos:", anos_disponiveis
)

oc_selecionados = st.sidebar.multiselect(
    "Selecione as variáveis de Excesso de Confiança Gerencial (opcional):", variaveis_oc
)

# Validação
if not niveis_selecionados:
    st.warning("Selecione pelo menos um nível de governança.")
    st.stop()

# Filtragem
df_filtrado = df.copy()

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]

# Filtrar por nível de governança
filtro_nivel = df_filtrado[niveis_selecionados].sum(axis=1) >= 1
df_filtrado = df_filtrado[filtro_nivel]

# Se filtrar por excesso de confiança
if oc_selecionados:
    filtro_oc = df_filtrado[oc_selecionados].sum(axis=1) >= 1
    df_filtrado = df_filtrado[filtro_oc]

# Verificar se há dados
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    # 📊 Geração do gráfico 
    st.subheader("📊 Comparativo: Governança vs. Excesso de Confiança")

    # Dados para o gráfico
    grafico_dados = []

    for nivel in niveis_selecionados:
        total_empresas = df_filtrado[df_filtrado[nivel] == 1].shape[0]
        if oc_selecionados:
            empresas_com_oc = df_filtrado[
                (df_filtrado[nivel] == 1) &
                (df_filtrado[oc_selecionados].sum(axis=1) >= 1)
            ].shape[0]
        else:
            empresas_com_oc = 0  # Nenhuma variável de OC selecionada

        grafico_dados.append({
            'Nível': nivel.upper(),
            'Total Empresas': total_empresas,
            'Empresas com OC': empresas_com_oc
        })

    grafico_df = pd.DataFrame(grafico_dados)

    fig = go.Figure()

    # Barras - Total de empresas
    fig.add_trace(go.Bar(
        x=grafico_df['Nível'],
        y=grafico_df['Total Empresas'],
        name='Total de Empresas',
        marker_color='lightskyblue'
    ))

    # Linha - Empresas com Excesso de Confiança
    fig.add_trace(go.Scatter(
        x=grafico_df['Nível'],
        y=grafico_df['Empresas com OC'],
        name='Empresas com OC',
        mode='lines+markers',
        marker=dict(size=8, color='firebrick'),
        line=dict(width=2, color='firebrick')
    ))

    fig.update_layout(
        title="Número de Empresas por Nível de Governança e Excesso de Confiança",
        xaxis_title="Nível de Governança",
        yaxis_title="Número de Empresas",
        bargap=0.4,
        template="simple_white"
    )

    st.plotly_chart(fig, use_container_width=True)

 
    # 📑 Exibição da tabela
    st.subheader("📑 Dados das Empresas Filtradas")
    st.dataframe(df_filtrado, use_container_width=True)

    # Download dos dados
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Empresas')

    st.download_button(
        label="📥 Baixar dados filtrados em Excel",
        data=output.getvalue(),
        file_name="empresas_filtradas_governanca.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
