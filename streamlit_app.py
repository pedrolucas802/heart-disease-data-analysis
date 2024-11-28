import altair as alt
import pandas as pd
import streamlit as st

# Configuração inicial do dashboard
st.set_page_config(
    page_title="Análise de Doenças Cardíacas", page_icon="❤️", layout="wide"
)
st.title("❤️ Análise de Dados de Doenças Cardíacas")
st.write("Explore padrões e insights sobre fatores de risco cardíacos")
st.write("TODO: COISAS DO KAGGLE")


# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_merged_heart_dataset.csv")

    valid_values = {
        "sex": [0, 1],
        "cp": [0, 1, 2, 3],
        "fbs": [0, 1],
        "restecg": [0, 1, 2],
        "exang": [0, 1],
        "slope": [0, 1, 2],
        "thal": [1, 2, 3],
        "target": [0, 1],
        "ca": [0, 1, 2, 3],
    }

    # Replace invalid values with "N/A" for categorical columns
    for column, valid in valid_values.items():
        if column in df.columns:
            df[column] = df[column].apply(lambda x: x if x in valid else "N/A")

    # Mapeia os valores categóricos para suas descrições
    df["sex"] = df["sex"].map({0: "Mulher", 1: "Homem", "N/A": "N/A"})
    df["cp"] = df["cp"].map(
        {
            0: "Angina típica",
            1: "Angina atípica",
            2: "Dor não anginal",
            3: "Assintomático",
            "N/A": "N/A",
        }
    )
    df["fbs"] = df["fbs"].map({0: "Falso", 1: "Verdadeiro", "N/A": "N/A"})
    df["restecg"] = df["restecg"].map(
        {
            0: "Normal",
            1: "Anormalidade ST-T",
            2: "Hipertrofia ventricular esquerda",
            "N/A": "N/A",
        }
    )
    df["exang"] = df["exang"].map({0: "Não", 1: "Sim", "N/A": "N/A"})
    df["slope"] = df["slope"].map(
        {0: "Ascendente", 1: "Plano", 2: "Descendente", "N/A": "N/A"}
    )
    df["thal"] = df["thal"].map(
        {1: "Normal", 2: "Defeito fixo", 3: "Defeito reversível", "N/A": "N/A"}
    )
    df["target"] = df["target"].map({0: "Menor risco", 1: "Maior risco", "N/A": "N/A"})

    return df