import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Heart Disease Prediction Dataset", page_icon="🫀")
st.title("🫀 Heart Disease Prediction Dataset")
st.write(
    """
    Welcome to the Heart Disease Prediction App! This application provides an interactive and
    user-friendly platform to explore, analyze, and visualize insights from the Heart Disease Prediction Dataset.
    """
)

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_merged_heart_dataset.csv")  # Adjust the file path if needed
    return df


df = load_data()

# Display the dataset preview
st.write("### Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# Add multiselect for categorical features
st.write("### Explore Features")
selected_features = st.multiselect(
    "Select Features to Visualize",
    ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalachh", "exang", "oldpeak", "slope", "ca", "thal", "target"],
    default=["age", "target"]
)

# Show a slider widget for filtering age
age_range = st.slider("Filter by Age", int(df["age"].min()), int(df["age"].max()), (30, 60))

# Filter the dataframe based on the widget input
df_filtered = df[(df["age"].between(age_range[0], age_range[1]))]

# Display the filtered data
st.write(f"### Filtered Data ({len(df_filtered)} rows)")
st.dataframe(df_filtered[selected_features], use_container_width=True)

# Visualization
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

# Additional Insights
st.write("### Summary Statistics")
st.write(df_filtered.describe())

# Add a note about the target feature
st.markdown(
    """
    **Note:**  
    - `target`: Indicates the presence of heart disease (1 = Disease, 0 = No Disease).  
    - Use the visualizations and statistics to explore correlations and trends in the data.
    """
)
