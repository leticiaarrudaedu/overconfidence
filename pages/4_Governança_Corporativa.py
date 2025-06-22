import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

# Título
st.title("Análise de Governança Corporativa e Excesso de Confiança Gerencial")

# Carregar dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# Padronizar colunas
df.columns = df.columns.str.lower()

# Colunas
niveis_governanca = ['n1', 'n2', 'nm']
variaveis_oc = ['oc1', 'oc2', 'oc3', 'oc4', 'oc134', 'oc234']

# Anos e opção todos
anos_disponiveis = sorted(df['ano'].dropna().unique())
anos_opcoes = ["Todos os anos"] + list(anos_disponiveis)

# Sidebar filtros
st.sidebar.header("Filtros")

# Seleção única para nível de governança
nivel_selecionado = st.sidebar.radio(
    "Nível de governança:",
    niveis_governanca,
    index=0
)

anos_selecionados = st.sidebar.multiselect(
    "Anos:",
    anos_opcoes,
    default=["Todos os anos"]
)

oc_selecionados = st.sidebar.multiselect(
    "Excesso de Confiança Gerencial (OC):",
    variaveis_oc
)

# Filtragem anos
df_base = df.copy()
if "Todos os anos" not in anos_selecionados and anos_selecionados:
    df_base = df_base[df_base['ano'].isin(anos_selecionados)]

# Filtrar pelo nível selecionado
df_nivel = df_base[df_base[nivel_selecionado] == 1]

# Preparar dados para gráfico por ano
dados_grafico = []
anos_para_grafico = sorted(df_nivel['ano'].dropna().unique())

for ano in anos_para_grafico:
    df_ano = df_nivel[df_nivel['ano'] == ano]
    total_empresas = df_ano.shape[0]
    if oc_selecionados:
        empresas_com_oc = df_ano[(df_ano[oc_selecionados].sum(axis=1) >= 1)].shape[0]
    else:
        empresas_com_oc = 0

    dados_grafico.append({
        'Ano': ano,
        'Total Empresas': total_empresas,
        'Empresas com OC': empresas_com_oc
    })

grafico_df = pd.DataFrame(dados_grafico)

# Construção do gráfico com azul e vermelho
st.subheader(f"Evolução: {nivel_selecionado.upper()}")

fig = go.Figure()

# Barra azul (total)
fig.add_trace(go.Bar(
    x=grafico_df['Ano'].astype(str),
    y=grafico_df['Total Empresas'],
    name='Total de Empresas',
    marker_color='rgba(0, 123, 255, 0.7)',
    hovertemplate='Ano: %{x}<br>Total de Empresas: %{y}<extra></extra>'
))

# Linha vermelha (excesso de confiança)
fig.add_trace(go.Scatter(
    x=grafico_df['Ano'].astype(str),
    y=grafico_df['Empresas com OC'],
    name='Empresas com Excesso de Confiança',
    mode='lines+markers',
    line=dict(color='crimson', width=3, shape='spline'),
    marker=dict(size=8, color='crimson'),
    hovertemplate='Ano: %{x}<br>Empresas com OC: %{y}<extra></extra>'
))

fig.update_layout(
    title=f"Número de Empresas por Ano - Nível {nivel_selecionado.upper()}",
    xaxis_title="Ano",
    yaxis_title="Número de Empresas",
    template="plotly_white",
    bargap=0.25,
    hovermode="x unified",
    barmode='group',
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

# Mostrar tabela filtrada depois do gráfico
st.subheader("📋 Dados representados no gráfico")

st.dataframe(df_nivel, use_container_width=True)

# Download Excel
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_nivel.to_excel(writer, index=False, sheet_name='Empresas')

st.download_button(
    label="Baixar dados filtrados em Excel",
    data=output.getvalue(),
    file_name=f"empresas_filtradas_{nivel_selecionado}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
