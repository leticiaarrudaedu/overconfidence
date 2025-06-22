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

# Definir colunas
niveis_governanca = ['n1', 'n2', 'nm']
variaveis_oc = ['oc1', 'oc2', 'oc3', 'oc4', 'oc134', 'oc234']

# Anos
anos_disponiveis = sorted(df['ano'].dropna().unique())
anos_opcoes = ["Todos os anos"] + list(anos_disponiveis)

# Sidebar de filtros
st.sidebar.header("Filtros")

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
    st.warning("Selecione pelo menos um nível de governança.")
    st.stop()

# Filtragem por ano (não filtrar se for "Todos os anos")
df_base = df.copy()

if "Todos os anos" not in anos_selecionados and anos_selecionados:
    df_base = df_base[df_base['ano'].isin(anos_selecionados)]

# Construção dos dados para o gráfico
dados_grafico = []

for nivel in niveis_selecionados:
    df_nivel = df_base[df_base[nivel] == 1]  # Filtrar empresas daquele nível

    for ano in sorted(df_nivel['ano'].dropna().unique()):
        df_ano = df_nivel[df_nivel['ano'] == ano]

        total_empresas = df_ano.shape[0]

        if oc_selecionados:
            empresas_com_oc = df_ano[
                (df_ano[oc_selecionados].sum(axis=1)) >= 1
            ].shape[0]
        else:
            empresas_com_oc = 0

        dados_grafico.append({
            'Ano': ano,
            'Nível': nivel.upper(),
            'Total Empresas': total_empresas,
            'Empresas com OC': empresas_com_oc
        })

grafico_df = pd.DataFrame(dados_grafico)

# Gráfico Interativo
st.subheader("Evolução: Governança e Excesso de Confiança por Ano")

fig = go.Figure()

# Adicionar barras e linhas por nível de governança
for nivel in grafico_df['Nível'].unique():
    dados_nivel = grafico_df[grafico_df['Nível'] == nivel]

    # Barras - Total de empresas
    fig.add_trace(go.Bar(
        x=dados_nivel['Ano'].astype(str),
        y=dados_nivel['Total Empresas'],
        name=f'{nivel} - Total',
        marker_color='rgba(0, 123, 255, 0.7)',
        hovertemplate='Ano: %{x}<br>Nível: '+nivel+'<br>Total de Empresas: %{y}<extra></extra>'
    ))

    # Linha - Empresas com OC
    fig.add_trace(go.Scatter(
        x=dados_nivel['Ano'].astype(str),
        y=dados_nivel['Empresas com OC'],
        name=f'{nivel} - Com OC',
        mode='lines+markers',
        line=dict(color='crimson', width=3, shape='spline'),
        marker=dict(size=8, color='crimson'),
        hovertemplate='Ano: %{x}<br>Nível: '+nivel+'<br>Empresas com OC: %{y}<extra></extra>'
    ))

fig.update_layout(
    title="Número de Empresas por Ano, Nível de Governança e Excesso de Confiança",
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

# Tabela dos Dados Filtrados
st.subheader("Dados das Empresas Filtradas")
df_tabela = df_base[
    (df_base[niveis_selecionados].sum(axis=1) >= 1)
]
st.dataframe(df_tabela, use_container_width=True)

# Download da tabela
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_tabela.to_excel(writer, index=False, sheet_name='Empresas')

st.download_button(
    label="Baixar dados filtrados em Excel",
    data=output.getvalue(),
    file_name="empresas_filtradas_governanca.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
