import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# === Leitura dos dados ===
df = pd.read_excel("dados.xlsx")

# === Título e descrição ===
st.title("Excesso de Confiança Gerencial e Desempenho")

st.write(
    "Utilize os filtros no menu lateral para selecionar os parâmetros e visualizar "
    "a comparação de desempenho entre empresas classificadas com excesso de confiança gerencial e aquelas sem o viés."
)

st.markdown("""
**Grupo 0:** Sem Excesso de Confiança Gerencial  
**Grupo 1:** Com Excesso de Confiança Gerencial
""")

# === Filtros no Sidebar ===
st.sidebar.header("🔎 Filtros Personalizados")

# Filtro de variável de grupo
coluna_filtro = st.sidebar.selectbox(
    "Escolha a variável de filtro:", 
    ['oc1', 'oc2', 'oc3', 'oc4', 'oc134', 'oc234']
)

# Filtro dos valores dessa variável
opcoes = sorted(df[coluna_filtro].dropna().unique())
valores_selecionados = st.sidebar.multiselect(
    f"Valores de {coluna_filtro}:", 
    opcoes, 
    default=opcoes
)

# Filtro da variável de desempenho
variavel_desempenho = st.sidebar.selectbox(
    "Variável de desempenho:", 
    ['wqtobin', 'wroa', 'wroaebit', 'wroe', 'wmgop']
)

# === Filtro por ano ===
anos_unicos = sorted(df['ano'].dropna().unique())
anos_opcoes = ["Todos"] + anos_unicos

anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos:", 
    anos_opcoes, 
    default=["Todos"]
)

if "Todos" in anos_selecionados:
    anos_filtrados = anos_unicos
else:
    anos_filtrados = anos_selecionados


# === Filtro por setor ===
setores_unicos = sorted(df['setor'].dropna().unique())
setores_opcoes = ["Todos"] + setores_unicos

setores_selecionados = st.sidebar.multiselect(
    "Selecione os setores:", 
    setores_opcoes, 
    default=["Todos"]
)

if "Todos" in setores_selecionados:
    setores_filtrados = setores_unicos
else:
    setores_filtrados = setores_selecionados


# === Aplicar filtros ===
df_filtrado = df[
    (df[coluna_filtro].isin(valores_selecionados)) & 
    (df['ano'].isin(anos_filtrados)) & 
    (df['setor'].isin(setores_filtrados))
]

# === Verificar e gerar gráfico ===
if variavel_desempenho in df_filtrado.columns:
    st.subheader(f"📉 Desempenho por Ano e Grupo de {coluna_filtro.upper()}")

    df_grouped = df_filtrado.groupby(['ano', coluna_filtro])[variavel_desempenho].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for grupo in sorted(df_grouped[coluna_filtro].dropna().unique()):
        subset = df_grouped[df_grouped[coluna_filtro] == grupo]
        ax3.plot(
            subset['ano'], 
            subset[variavel_desempenho], 
            marker='o', 
            label=f'Grupo {grupo}'
        )

    ax3.set_title(f"{variavel_desempenho.upper()} Médio por Ano e {coluna_filtro.upper()}")
    ax3.set_xlabel("Ano")
    ax3.set_ylabel(f"{variavel_desempenho.upper()} Médio")
    ax3.set_xticks(sorted(df_grouped['ano'].unique()))
    ax3.grid(True)
    ax3.legend(title=coluna_filtro.upper())
    plt.tight_layout()

    st.pyplot(fig3)

    # === Mostrar tabela dos dados filtrados ===
    st.subheader("📋 Dados representados no gráfico")
    st.dataframe(df_filtrado, use_container_width=True)

    # === Download dos dados em Excel ===
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Dados_Filtrados')
    output.seek(0)

    st.download_button(
        label="Baixar dados em Excel",
        data=output.getvalue(),
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning(f"⚠️ A coluna '{variavel_desempenho}' não está disponível no DataFrame.")
