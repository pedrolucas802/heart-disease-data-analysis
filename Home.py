import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Heart Disease Prediction Dataset", page_icon="🫀")
st.title("🫀 Heart Disease Prediction Dataset")
st.write(
    """
    Welcome to the Heart Disease Prediction App! This application provides an interactive and
    user-friendly platform to explore, analyze, and visualize insights from the Heart Disease Prediction Dataset.
    """
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_merged_heart_dataset.csv")
    return df


df = load_data()

# Display the dataset preview
st.write("### Dataset Preview")
st.dataframe(df.head(), use_container_width=True)
