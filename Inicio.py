import altair as alt
import pandas as pd
import streamlit as st

# Configuração inicial do dashboard
st.set_page_config(
    page_title="Análise de Doenças Cardíacas", page_icon="❤️", layout="wide"
)
st.title("❤️ Análise de Dados de Doenças Cardíacas")

st.write("""
Este conjunto de dados remonta a 1988 e é composto por quatro bases de dados: Cleveland, Hungria, Suíça e Long Beach V. Ele contém 76 atributos, incluindo o atributo previsto, mas todos os experimentos publicados fazem referência ao uso de um subconjunto de 14 desses atributos.
""")

# O campo **"target"** refere-se à presença de doença cardíaca no paciente. Ele possui valores inteiros:
# - **0**: Sem doença.
# - **1**: Com doença.


st.title("📋 Descrição das Variáveis do Conjunto de Dados")

st.write("""
Este conjunto de dados contém informações relacionadas à saúde cardíaca. As variáveis disponíveis são descritas abaixo:

- **Age**: Idade do paciente.
- **Sex**: Gênero do paciente (0 = Mulher, 1 = Homem).
- **Chest Pain Type (4 values)**: Tipo de dor no peito:
  - 0: Angina típica
  - 1: Angina atípica
  - 2: Dor não relacionada ao coração
  - 3: Assintomática
- **Resting Blood Pressure**: Pressão arterial em repouso (mm Hg).
- **Serum Cholestoral in mg/dl**: Nível de colesterol sérico em mg/dl.
- **Fasting Blood Sugar > 120 mg/dl**: Glicemia de jejum > 120 mg/dl (1 = Verdadeiro, 0 = Falso).
- **Resting Electrocardiographic Results (values 0, 1, 2)**: Resultados do eletrocardiograma em repouso:
  - 0: Normal
  - 1: Anormalidade na onda ST-T (inversão da onda T ou elevação/abaixamento do segmento ST > 0,05 mV)
  - 2: Hipertrofia ventricular esquerda provável ou definitiva.
- **Maximum Heart Rate Achieved**: Frequência cardíaca máxima atingida durante o teste.
- **Exercise Induced Angina**: Angina induzida por exercício (1 = Sim, 0 = Não).
- **Oldpeak**: Depressão do segmento ST induzida por exercício em relação ao repouso.
- **The Slope of the Peak Exercise ST Segment**: Inclinação do segmento ST no pico do exercício:
  - 0: Declive
  - 1: Plano
  - 2: Ascendente.
- **Number of Major Vessels (0-3) Colored by Flourosopy**: Número de principais vasos sanguíneos (0-3) coloridos por fluoroscopia.
- **Thal**: Resultado do exame de thalassemia:
  - 0: Normal
  - 1: Defeito fixo
  - 2: Defeito reversível.
""")


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