import altair as alt
import pandas as pd
import streamlit as st

# Função para carregar os dados
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_merged_heart_dataset.csv")


# Carregar os dados
df = load_data()

st.title("Análise de Dados de Saúde Cardíaca")

# Filtros gerais
st.write("## Filtros Gerais")
age_range = st.slider(
    "Filtrar por faixa etária",
    int(df["age"].min()),
    int(df["age"].max()),
    (30, 60)
)

sex_filter = st.radio(
    "Filtrar por Sexo",
    options=["Todos", "Masculino", "Feminino"],
    index=0
)

target_filter = st.checkbox("Mostrar apenas pacientes com doença cardíaca (target = 1)")

# Aplicar filtros gerais
df_filtered = df[df["age"].between(age_range[0], age_range[1])]

if sex_filter == "Masculino":
    df_filtered = df_filtered[df_filtered["sex"] == 1]
elif sex_filter == "Feminino":
    df_filtered = df_filtered[df_filtered["sex"] == 0]

if target_filter:
    df_filtered = df_filtered[df_filtered["target"] == 1]

st.write(f"### Dados Filtrados ({len(df_filtered)} linhas)")
st.dataframe(df_filtered, use_container_width=True)

# Estatísticas Resumidas
st.write("## Estatísticas Resumidas")
selected_features = st.multiselect(
    "Selecione as características para visualizar estatísticas",
    df.columns.tolist(),
    default=["age", "target"]
)

if selected_features:
    summary_stats = (
        df_filtered[selected_features]
        .describe()
        .transpose()
        .reset_index()
        .rename(columns={"index": "Feature"})
    )
    st.write(summary_stats)

    st.write("### Gráficos de Estatísticas")
    stat_option = st.radio(
        "Escolha o tipo de estatística para visualizar",
        options=["Máximo e Mínimo", "Média", "Mediana"],
        index=0
    )

    if stat_option == "Máximo e Mínimo":
        stat_data = summary_stats.melt(
            id_vars=["Feature"],
            value_vars=["min", "max"],
            var_name="Statistic",
            value_name="Value"
        )
        chart = alt.Chart(stat_data).mark_bar().encode(
            x="Feature:N",
            y="Value:Q",
            color="Statistic:N",
            tooltip=["Feature", "Statistic", "Value"]
        )
        st.altair_chart(chart, use_container_width=True)

    elif stat_option == "Média":
        chart = alt.Chart(summary_stats).mark_bar().encode(
            x="Feature:N",
            y="mean:Q",
            tooltip=["Feature", "mean"]
        )
        st.altair_chart(chart, use_container_width=True)

    elif stat_option == "Mediana":
        chart = alt.Chart(summary_stats).mark_point(filled=True, size=100).encode(
            x="Feature:N",
            y="50%:Q",
            tooltip=["Feature", "50%"]
        )
        st.altair_chart(chart, use_container_width=True)

# Gráfico Personalizado
st.write("## Gráficos Personalizados")
chart_type = st.selectbox(
    "Escolha o tipo de gráfico",
    options=["Barras", "Linhas", "Dispersão"],
    index=0
)

x_axis = st.selectbox("Selecione a variável para o eixo X", options=df.columns)
y_axis = st.selectbox("Selecione a variável para o eixo Y", options=df.columns)

if chart_type == "Barras":
    chart = alt.Chart(df_filtered).mark_bar().encode(
        x=f"{x_axis}:Q",
        y=f"{y_axis}:Q",
        color="target:N",
        tooltip=[x_axis, y_axis, "target"]
    )
elif chart_type == "Linhas":
    chart = alt.Chart(df_filtered).mark_line().encode(
        x=f"{x_axis}:Q",
        y=f"{y_axis}:Q",
        color="target:N",
        tooltip=[x_axis, y_axis, "target"]
    )
elif chart_type == "Dispersão":
    chart = alt.Chart(df_filtered).mark_circle(size=75).encode(
        x=f"{x_axis}:Q",
        y=f"{y_axis}:Q",
        color="target:N",
        tooltip=[x_axis, y_axis, "target"]
    )
st.altair_chart(chart, use_container_width=True)
