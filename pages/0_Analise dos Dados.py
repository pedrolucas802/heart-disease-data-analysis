import altair as alt
import pandas as pd
import streamlit as st

from streamlit_app import load_data

# Carregar dataset
df = load_data()

# Header: Estatísticas gerais
st.subheader("📊 Estatísticas Gerais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Média de Idade", f"{df['age'].mean():.1f} anos")

with col2:
    male_count = df[df["sex"] == "Homem"].shape[0]
    female_count = df[df["sex"] == "Mulher"].shape[0]
    st.metric("Proporção Homens/Mulheres", f"{male_count}/{female_count}")

with col3:
    risk_positive = (df["target"] == "Maior risco").mean() * 100
    st.metric("Risco de Ataque Cardíaco", f"{risk_positive:.1f}% com maior risco")

with col4:
    st.metric("Média de Colesterol", f"{df['chol'].mean():.1f} mg/dL")

with col5:
    high_fbs = (df["fbs"] == "Verdadeiro").mean() * 100
    st.metric("Taxa de Açúcar Elevado", f"{high_fbs:.1f}%")

# Seção: Análise de Fatores de Risco
st.subheader("📈 Análise de Fatores de Risco")

# Idade e Gênero
st.write("### Idade e Gênero")
col1, col2 = st.columns(2)

with col1:
    bar_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("sex:N", title="Gênero"),
            y=alt.Y("count():Q", title="Número de Pacientes"),
            color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
            tooltip=["sex", "count()", "target"],
        )
        .properties(title="Distribuição de Risco por Gênero")
    )
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    box_chart = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X("target:N", title="Risco de Ataque Cardíaco"),
            y=alt.Y("age:Q", title="Idade"),
            color=alt.Color("target:N", title="Risco"),
            tooltip=["age", "target"],
        )
        .properties(title="Faixa Etária por Risco de Ataque Cardíaco")
    )
    st.altair_chart(box_chart, use_container_width=True)

# Dor no Peito
st.write("### Dor no Peito")
cp_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("cp:N", title="Tipo de Dor no Peito"),
        y=alt.Y("count():Q", title="Número de Pacientes"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["cp", "count()", "target"],
    )
    .properties(title="Tipos de Dor no Peito vs. Risco de Ataque Cardíaco")
)
st.altair_chart(cp_chart, use_container_width=True)

# Pressão Sanguínea e Colesterol
st.write("### Pressão Sanguínea e Colesterol")
scatter_chart = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x=alt.X("trestbps:Q", title="Pressão Sanguínea em Repouso (mm Hg)"),
        y=alt.Y("chol:Q", title="Colesterol Sérico (mg/dL)"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["trestbps", "chol", "target"],
    )
    .properties(title="Relação entre Pressão Sanguínea e Colesterol")
)
st.altair_chart(scatter_chart, use_container_width=True)

# Frequência Cardíaca Máxima
st.write("### Frequência Cardíaca Máxima")
hist_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("thalach:Q", bin=True, title="Frequência Cardíaca Máxima (bpm)"),
        y=alt.Y("count():Q", title="Número de Pacientes"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["thalach", "count()", "target"],
    )
    .properties(title="Distribuição de Frequência Cardíaca por Categoria de Risco")
)
st.altair_chart(hist_chart, use_container_width=True)

# Exercício e ECG
st.write("### Exercício e ECG")
exang_ecg_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("restecg:N", title="Resultados do ECG em Repouso"),
        y=alt.Y("count():Q", title="Número de Pacientes"),
        color=alt.Color("exang:N", title="Angina Induzida por Exercício"),
        tooltip=["restecg", "count()", "exang"],
    )
    .properties(title="Distribuição de ECG e Exercício por Risco")
)
st.altair_chart(exang_ecg_chart, use_container_width=True)

# Análise Avançada
st.subheader("📊 Análise Avançada")

# Heatmap: slope, oldpeak e risco
st.write("### Relação entre Slope, Oldpeak e Risco")
heatmap = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X("slope:N", title="Inclinação do Segmento ST"),
        y=alt.Y("oldpeak:Q", title="Depressão do Segmento ST"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["slope", "oldpeak", "target"],
    )
    .properties(title="Heatmap: Slope vs Oldpeak vs Risco")
)
st.altair_chart(heatmap, use_container_width=True)

# Thalassemia
st.write("### Tipos de Thalassemia")
thal_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("thal:N", title="Tipo de Thalassemia"),
        y=alt.Y("count():Q", title="Número de Pacientes"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["thal", "count()", "target"],
    )
    .properties(title="Distribuição de Thalassemia por Categoria de Risco")
)
st.altair_chart(thal_chart, use_container_width=True)

# Número de vasos
st.write("### Número de Vasos e Risco")
scatter_vessels = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x=alt.X("ca:Q", title="Número de Vasos Principais"),
        y=alt.Y("oldpeak:Q", title="Depressão do Segmento ST"),
        color=alt.Color("target:N", title="Risco de Ataque Cardíaco"),
        tooltip=["ca", "oldpeak", "target"],
    )
    .properties(title="Relação entre Número de Vasos e Depressão do Segmento ST")
)
st.altair_chart(scatter_vessels, use_container_width=True)
