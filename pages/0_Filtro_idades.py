import altair as alt
import pandas as pd
import streamlit as st

from main import load_data

df = load_data()

st.write("### Explore os dados por idade")
selected_features = st.multiselect(
    "Select Features to Visualize",
    ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalachh", "exang", "oldpeak", "slope", "ca", "thal", "target"],
    default=["age", "target"]
)

age_range = st.slider("Filter by Age", int(df["age"].min()), int(df["age"].max()), (30, 60))

df_filtered = df[(df["age"].between(age_range[0], age_range[1]))]

st.write(f"### Filtered Data ({len(df_filtered)} rows)")
st.dataframe(df_filtered[selected_features], use_container_width=True)

st.write("### Visualize Relationships")
if "age" in selected_features and "target" in selected_features:
    chart = (
        alt.Chart(df_filtered)
        .mark_circle(size=60)
        .encode(
            x=alt.X("age:Q", title="Age"),
            y=alt.Y("target:Q", title="Heart Disease Presence (1=Yes, 0=No)"),
            color="target:N",
            tooltip=["age", "target", "chol", "thalachh"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

st.write("### Summary Statistics")
st.write(df_filtered.describe())

st.markdown(
    """
    **Note:**  
    - `target`: Indicates the presence of heart disease (1 = Disease, 0 = No Disease).  
    - Use the visualizations and statistics to explore correlations and trends in the data.
    """
)
