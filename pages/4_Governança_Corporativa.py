import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import plotly.express as px

# Título
st.title("Análise de Governança Corporativa e Excesso de Confiança Gerencial")

# Carregamento dos dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# Colunas minúsculas
df.columns = df.columns.str.lower()

# Definir variáveis
niveis_governanca = ['n1', 'n2', 'nm']
variaveis_oc = ['oc1', 'oc2', 'oc3', 'oc4', 'oc134', 'oc234']

# Anos
anos_disponiveis = sorted(df['ano'].dropna().unique())
anos_opcoes = ["Todos os anos"] + list(anos_disponiveis)

# Sidebar de filtros
st.sidebar.header("🔍 Filtros")

niveis_selecionados = st.sidebar.multiselect(
    "Níveis de governança:", niveis_governanca
)

anos_selecionados = st.sidebar.multiselect(
    "Anos:", anos_opcoes, default="Todos os anos"
)

oc_selecionados = st.sidebar.multiselect(
    "Excesso de Confiança Gerencial (OC):", variaveis_oc
)

# Validação
if not niveis_selecionados:
    st.warning("⚠️ Selecione pelo menos um nível de governança.")
    st.stop()

# Filtragem
df_filtrado = df.copy()

# Filtro de ano
if "Todos os anos" not in anos_selecionados and anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]

# Filtrar por nível de governança
filtro_nivel = df_filtrado[niveis_selecionados].sum(axis=1) >= 1
df_filtrado = df_filtrado[filtro_nivel]

# Filtrar por OC se selecionado
if oc_selecionados:
    filtro_oc = df_filtrado[oc_selecionados].sum(axis=1) >= 1
    df_filtrado = df_filtrado[filtro_oc]

# Validação de dados
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
else:

    # Gráfico
    st.subheader("📊 Evolução Anual: Governança e Excesso de Confiança")

    grafico_dados = []

    for ano in sorted(df_filtrado['ano'].unique()):
        dados_ano = df_filtrado[df_filtrado['ano'] == ano]

        total_empresas = dados_ano[
            dados_ano[niveis_selecionados].sum(axis=1) >= 1
        ].shape[0]

        if oc_selecionados:
            empresas_com_oc = dados_ano[
                (dados_ano[niveis_selecionados].sum(axis=1) >= 1) &
                (dados_ano[oc_selecionados].sum(axis=1) >= 1)
            ].shape[0]
        else:
            empresas_com_oc = 0

        grafico_dados.append({
            'Ano': ano,
            'Total Empresas': total_empresas,
            'Empresas com OC': empresas_com_oc
        })

    grafico_df = pd.DataFrame(grafico_dados)

    fig = go.Figure()

    # Barras - Total de empresas
    fig.add_trace(go.Bar(
        x=grafico_df['Ano'].astype(str),
        y=grafico_df['Total Empresas'],
        name='Total de Empresas',
        marker_color='rgba(0, 123, 255, 0.8)',
        hovertemplate='Ano: %{x}<br>Total de Empresas: %{y}<extra></extra>'
    ))

    # Linha - Empresas com OC
    fig.add_trace(go.Scatter(
        x=grafico_df['Ano'].astype(str),
        y=grafico_df['Empresas com OC'],
        name='Empresas com OC',
        mode='lines+markers',
        line=dict(color='crimson', width=3, shape='spline'),
        marker=dict(size=8, color='crimson'),
        hovertemplate='Ano: %{x}<br>Empresas com OC: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title="📈 Número de Empresas por Ano e Excesso de Confiança",
        xaxis_title="Ano",
        yaxis_title="Número de Empresas",
        template="plotly_white",
        bargap=0.3,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # 📑 Exibição da Tabela
    st.subheader("📑 Dados das Empresas Filtradas")
    st.dataframe(df_filtrado, use_container_width=True)

    # Exportar dados
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Empresas')

    st.download_button(
        label="📥 Baixar dados filtrados em Excel",
        data=output.getvalue(),
        file_name="empresas_filtradas_governanca.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
