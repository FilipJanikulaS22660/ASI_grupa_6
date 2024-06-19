import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path
import numpy as np

# Uzyskanie ścieżki do katalogu głównego projektu
project_path = Path(__file__).resolve().parent

# Inicjalizacja projektu Kedro
bootstrap_project(project_path)

# Tworzenie sesji Kedro
with KedroSession.create(project_path=project_path) as session:
    context = session.load_context()
    catalog = context.catalog

    # Załaduj wytrenowany model
    predictor = catalog.load('autoML_model')

    # Funkcja do wykonywania predykcji na podstawie danych wejściowych
    def predict_health_condition(input_data: pd.DataFrame):
        prediction = predictor.predict(input_data)
        return prediction[0]

    # Mappings for label encoding
    mappings = {
        'Smoking': {'Yes': 1, 'No': 0},
        'AlcoholDrinking': {'Yes': 1, 'No': 0},
        'Stroke': {'Yes': 1, 'No': 0},
        'DiffWalking': {'Yes': 1, 'No': 0},
        'Sex': {'Male': 1, 'Female': 0},
        'AgeCategory': {'18-24': 0, '25-29': 1, '30-34': 2, '35-39': 3, '40-44': 4, '45-49': 5, '50-54': 6, '55-59': 7, '60-64': 8, '65-69': 9, '70-74': 10, '75-79': 11, '80 or older': 12},
        'Race': {'White': 0, 'Black': 1, 'Asian': 2, 'Native': 3, 'Hispanic': 4, 'Other': 5},
        'Diabetic': {'Yes': 1, 'No': 0, 'No, borderline diabetes': 2, 'Yes (during pregnancy)': 3},
        'PhysicalActivity': {'Yes': 1, 'No': 0},
        'GenHealth': {'Excellent': 0, 'Very good': 1, 'Good': 2, 'Fair': 3, 'Poor': 4},
        'Asthma': {'Yes': 1, 'No': 0},
        'KidneyDisease': {'Yes': 1, 'No': 0},
        'SkinCancer': {'Yes': 1, 'No': 0}
    }

    # Funkcja do mapowania wartości kategorycznych na liczby
    def map_values(df, mappings):
        for col, mapping in mappings.items():
            df[col] = df[col].map(mapping)
        return df

    # Strona główna Streamlit
    st.title("Health Condition Prediction")

    # Formularz do wprowadzania danych
    st.header("Enter Health Details")

    bmi = st.number_input('BMI', min_value=0.0)
    smoking = st.selectbox('Smoking', ['Yes', 'No'])
    alcohol_drinking = st.selectbox('Alcohol Drinking', ['Yes', 'No'])
    stroke = st.selectbox('Stroke', ['Yes', 'No'])
    physical_health = st.number_input('Physical Health (days)', min_value=0, max_value=30)
    mental_health = st.number_input('Mental Health (days)', min_value=0, max_value=30)
    diff_walking = st.selectbox('Difficulty Walking', ['Yes', 'No'])
    sex = st.selectbox('Sex', ['Male', 'Female'])
    age_category = st.selectbox('Age Category', ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older'])
    race = st.selectbox('Race', ['White', 'Black', 'Asian', 'Native', 'Hispanic', 'Other'])
    diabetic = st.selectbox('Diabetic', ['Yes', 'No', 'No, borderline diabetes', 'Yes (during pregnancy)'])
    physical_activity = st.selectbox('Physical Activity', ['Yes', 'No'])
    gen_health = st.selectbox('General Health', ['Excellent', 'Very good', 'Good', 'Fair', 'Poor'])
    sleep_time = st.number_input('Sleep Time (hours)', min_value=0, max_value=24)
    asthma = st.selectbox('Asthma', ['Yes', 'No'])
    kidney_disease = st.selectbox('Kidney Disease', ['Yes', 'No'])
    skin_cancer = st.selectbox('Skin Cancer', ['Yes', 'No'])

    # Tworzymy DataFrame z wprowadzonymi danymi
    input_data = pd.DataFrame({
        'BMI': [bmi],
        'Smoking': [smoking],
        'AlcoholDrinking': [alcohol_drinking],
        'Stroke': [stroke],
        'PhysicalHealth': [physical_health],
        'MentalHealth': [mental_health],
        'DiffWalking': [diff_walking],
        'Sex': [sex],
        'AgeCategory': [age_category],
        'Race': [race],
        'Diabetic': [diabetic],
        'PhysicalActivity': [physical_activity],
        'GenHealth': [gen_health],
        'SleepTime': [sleep_time],
        'Asthma': [asthma],
        'KidneyDisease': [kidney_disease],
        'SkinCancer': [skin_cancer]
    })

    # Mapowanie wartości kategorycznych na liczby
    input_data = map_values(input_data, mappings)

    if st.button('Predict Health Condition'):
        # Wykonaj predykcję
        condition = predict_health_condition(input_data)
        st.write(f'The predicted health condition is: {condition}')