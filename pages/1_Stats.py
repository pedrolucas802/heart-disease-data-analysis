import altair as alt
import pandas as pd
import streamlit as st

from home import load_data


df = load_data()

st.header("A. Estatísticas Gerais")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Média de Idade", f"{df['age'].mean():.1f} anos")
col2.metric("Proporção Homens/Mulheres", f"{df['sex'].value_counts(normalize=True)[1]*100:.1f}% / {df['sex'].value_counts(normalize=True)[0]*100:.1f}%")
col3.metric("Risco de Ataque Cardíaco", f"{df['target'].value_counts(normalize=True)[1]*100:.1f}% com risco")
col4.metric("Média de Colesterol", f"{df['chol'].mean():.1f} mg/dL")
col5.metric("Pacientes com Açúcar Elevado", f"{df['fbs'].mean()*100:.1f}%")

st.header("B. Análise de Fatores de Risco")

st.subheader("Idade e Gênero")

st.write("Distribuição do risco de ataque cardíaco por gênero")
gender_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="sex:N",
        y="count()",
        color="target:N",
        column="target:N",
        tooltip=["count()"]
    )
    .properties(width=200)
)
st.altair_chart(gender_chart, use_container_width=True)

st.write("Faixa etária por risco de ataque cardíaco")
age_risk_boxplot = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x="target:N",
        y="age:Q",
        color="target:N",
        tooltip=["age"]
    )
)
st.altair_chart(age_risk_boxplot, use_container_width=True)

st.subheader("Dor no Peito (cp)")

cp_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="cp:N",
        y="count()",
        color="target:N",
        tooltip=["cp", "count()"]
    )
)
st.altair_chart(cp_chart, use_container_width=True)

st.subheader("Pressão Sanguínea e Colesterol")

bp_chol_chart = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x="trestbps:Q",
        y="chol:Q",
        color="target:N",
        tooltip=["trestbps", "chol", "target"]
    )
)
st.altair_chart(bp_chol_chart, use_container_width=True)
