import streamlit as st
import pandas as pd
import io

# Título
st.title("Empresas por Nível de Governança Corporativa e Ano")

# Carregamento dos dados
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados.xlsx' não encontrado.")
    st.stop()

# Garantir nomes em minúsculo para evitar erros
df.columns = df.columns.str.lower()

# Níveis disponíveis (colunas)
niveis_governanca = ['n1', 'n2', 'nm']

# Anos disponíveis (assumindo que há uma coluna 'ano')
anos_disponiveis = sorted(df['ano'].dropna().unique())

# Filtros interativos
niveis_selecionados = st.multiselect("Selecione os níveis de governança:", niveis_governanca)
anos_selecionados = st.multiselect("Selecione os anos:", anos_disponiveis)

# Validação
if not niveis_selecionados:
    st.warning("Selecione pelo menos um nível de governança.")
    st.stop()

# Filtragem
df_filtrado = df.copy()

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]

# Filtrar linhas que tenham valor 1 em pelo menos um dos níveis selecionados
filtro_nivel = df_filtrado[niveis_selecionados].sum(axis=1) >= 1
df_filtrado = df_filtrado[filtro_nivel]

# Exibição da tabela
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    st.subheader("Dados das Empresas Filtradas")
    st.dataframe(df_filtrado, use_container_width=True)

    # Exportar para Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Empresas')

    st.download_button(
        label="📥 Baixar dados filtrados em Excel",
        data=output.getvalue(),
        file_name="empresas_filtradas_governanca.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
