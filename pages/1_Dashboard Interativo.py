import pandas as pd
import plotly.express as px
import streamlit as st

from Inicio import load_data

# Carregar dataset
df = load_data()

# Converter colunas numéricas corretamente, caso estejam como strings
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    except ValueError:
        pass

st.title("Análise Interativa de Dados de Saúde Cardíaca")

# Filtros para o usuário
st.write("## Filtros de Dados")

# Criar um filtro para cada coluna do dataset
filters = {}
for col in df.columns:
    if df[col].dtype == 'object' or df[col].nunique() < 20:  # Colunas categóricas ou com poucos valores únicos
        filters[col] = st.multiselect(f"{col.capitalize()}", options=df[col].unique(), default=df[col].unique())
    elif pd.api.types.is_numeric_dtype(df[col]):  # Colunas numéricas
        col_min, col_max = float(df[col].min()), float(df[col].max())
        
        # Checar se os valores são inteiros para ajustar o slider
        if col_min.is_integer() and col_max.is_integer():
            filters[col] = st.slider(
                f"{col.capitalize()}",
                int(col_min), int(col_max),
                (int(col_min), int(col_max))
            )
        else:
            filters[col] = st.slider(
                f"{col.capitalize()}",
                round(col_min, 2), round(col_max, 2),
                (round(col_min, 2), round(col_max, 2))
            )

# Aplicar os filtros no DataFrame
for col, filter_value in filters.items():
    if isinstance(filter_value, list):  # Multiselect
        df = df[df[col].isin(filter_value)]
    elif isinstance(filter_value, tuple):  # Slider
        df = df[df[col].between(filter_value[0], filter_value[1])]

# Checkbox para mostrar ou ocultar a tabela de dados filtrados
show_table = st.checkbox("Mostrar tabela de dados filtrados", value=True)

if show_table:
    st.write(f"### Dados Filtrados ({len(df)} linhas)")
    st.dataframe(df)

# Seleção de variáveis para gráficos
st.write("## Gráficos Interativos")
x_axis = st.selectbox("Selecione a variável para o eixo X", options=df.columns, index=0)
y_axis = st.selectbox(
    "Selecione a variável para o eixo Y",
    options=df.select_dtypes(include=["number"]).columns,
    index=1,
)

# Escolha do tipo de gráfico
chart_type = st.radio("Escolha o tipo de gráfico", ["Dispersão", "Linhas"], index=0)

# Gerar gráficos de dispersão ou linhas
if chart_type == "Dispersão":
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color="target" if "target" in df.columns else None,
        title=f"Gráfico de Dispersão ({x_axis} vs {y_axis})",
        labels={x_axis: x_axis.capitalize(), y_axis: y_axis.capitalize()},
    )
elif chart_type == "Linhas":
    fig = px.line(
        df,
        x=x_axis,
        y=y_axis,
        color="target" if "target" in df.columns else None,
        title=f"Gráfico de Linhas ({x_axis} vs {y_axis})",
        labels={x_axis: x_axis.capitalize(), y_axis: y_axis.capitalize()},
    )

# Exibir o gráfico (Dispersão ou Linhas)
st.plotly_chart(fig, use_container_width=True)
