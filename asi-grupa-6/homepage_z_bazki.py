import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor
from sqlalchemy import create_engine, text
from pathlib import Path
import pickle

# Utwórz połączenie z bazą danych
# Użyj pg8000 zamiast psycopg2
engine = create_engine('postgresql+pg8000://kedro_user:password@localhost:5432/kedro_db')

# Funkcja do pobierania dostępnych modeli z bazy danych
def fetch_models_from_db(engine):
    query = text("SELECT name FROM models")
    with engine.connect() as connection:
        result = connection.execute(query)
        models = result.fetchall()
    return [model[0] for model in models]

# Funkcja do wczytywania wybranego modelu z bazy danych
def load_model_from_db(engine, model_name):
    query = text("SELECT model FROM models WHERE name = :name")
    with engine.connect() as connection:
        result = connection.execute(query, {"name": model_name})
        model_data = result.fetchone()
    if model_data:
        return pickle.loads(model_data[0])
    return None

# Załaduj dostępne modele
model_names = fetch_models_from_db(engine)

# Strona główna Streamlit
st.title("Health Condition Prediction")

# Wyświetl listę rozwijaną z modelami
selected_model_name = st.selectbox("Wybierz model", model_names)

# Wczytaj wybrany model
predictor = load_model_from_db(engine, selected_model_name)

# Funkcja do wykonywania predykcji na podstawie danych wejściowych
def predict_health_condition(input_data: pd.DataFrame):
    try:
        if predictor:
            prediction = predictor.predict(input_data)
            return prediction[0]
        else:
            st.error("Model nie został poprawnie załadowany.")
            return None
    except AttributeError as e:
        st.error(f"Błąd podczas predykcji: {e}")
        return None

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

if st.button('Predict Health Condition') and predictor:
    # Wykonaj predykcję
    condition = predict_health_condition(input_data)
    if condition is not None:
        st.write(f'The predicted health condition is: {condition}')