import altair as alt
import pandas as pd
import streamlit as st

# Configuração inicial do dashboard
st.set_page_config(
    page_title="Análise de Doenças Cardíacas", page_icon="❤️", layout="wide"
)
st.title("❤️ Análise de Dados de Doenças Cardíacas")
st.write("Explore padrões e insights sobre fatores de risco cardíacos")


# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_merged_heart_dataset.csv")
    return df


# Carregar dataset
df = load_data()

# Header: Estatísticas gerais
st.subheader("📊 Estatísticas Gerais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Média de Idade", f"{df['age'].mean():.1f} anos")

with col2:
    male_count = df[df["sex"] == 1].shape[0]
    female_count = df[df["sex"] == 0].shape[0]
    st.metric("Proporção Homens/Mulheres", f"{male_count}/{female_count}")

with col3:
    risk_positive = (df["target"] == 1).mean() * 100
    st.metric("Risco de Ataque Cardíaco", f"{risk_positive:.1f}% com risco")

with col4:
    st.metric("Média de Colesterol", f"{df['chol'].mean():.1f} mg/dL")

with col5:
    high_fbs = (df["fbs"] == 1).mean() * 100
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
            x="sex:N",
            y="count():Q",
            color="target:N",
            tooltip=["sex", "count()", "target"],
        )
        .properties(title="Distribuição de Risco por Gênero")
    )
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    box_chart = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(x="target:N", y="age:Q", color="target:N", tooltip=["age", "target"])
        .properties(title="Faixa Etária por Risco de Ataque Cardíaco")
    )
    st.altair_chart(box_chart, use_container_width=True)

# Dor no Peito
st.write("### Dor no Peito")
cp_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="cp:N", y="count():Q", color="target:N", tooltip=["cp", "count()", "target"]
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
        x="trestbps:Q",
        y="chol:Q",
        color="target:N",
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
        x=alt.X("thalachh:Q", bin=True),
        y="count():Q",
        color="target:N",
        tooltip=["thalachh", "count()", "target"],
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
        x="restecg:N",
        y="count():Q",
        color="exang:N",
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
        x="slope:N",
        y="oldpeak:Q",
        color="target:N",
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
        x="thal:N",
        y="count():Q",
        color="target:N",
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
        x="ca:Q", y="oldpeak:Q", color="target:N", tooltip=["ca", "oldpeak", "target"]
    )
    .properties(title="Relação entre Vasos, Oldpeak e Risco")
)
st.altair_chart(scatter_vessels, use_container_width=True)
