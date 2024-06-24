import os
import pickle
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Utwórz połączenie z bazą danych (odkomentuj wybrany sterownik)
# Użycie pg8000
# engine = create_engine('postgresql+pg8000://kedro_user:password@localhost:5432/kedro_db')

# Użycie psycopg2
engine = create_engine('postgresql+psycopg2://kedro_user:password@localhost:5432/kedro_db')

# Ścieżka do głównego folderu z modelami
base_path = "AutogluonModels"

# Funkcja do znalezienia najnowszego folderu
def get_latest_folder(base_path):
    all_folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    latest_folder = max(all_folders, key=os.path.getmtime)
    return latest_folder

# Pobierz najnowszy folder
latest_folder = get_latest_folder(base_path)
models_path = os.path.join(latest_folder, "models")

# Funkcja do zapisywania modelu do bazy danych
def save_model_to_db(model_name, model_path, engine):
    with open(model_path, 'rb') as file:
        model_data = file.read()

    # Zapisz model do bazy danych
    query = text("""
    INSERT INTO models (name, model)
    VALUES (:name, :model)
    ON CONFLICT (name) DO UPDATE
    SET model = EXCLUDED.model;
    """)
    try:
        with engine.begin() as connection:
            connection.execute(query, {"name": model_name, "model": model_data})
    except (OperationalError, ProgrammingError) as e:
        print(f"Błąd podczas zapisu modelu {model_name}: {e}")

# Iteruj przez wszystkie modele w folderze
for model_name in os.listdir(models_path):
    model_folder_path = os.path.join(models_path, model_name)
    model_file_path = os.path.join(model_folder_path, "model.pkl")
    
    # Sprawdź, czy ścieżka jest katalogiem i czy zawiera plik model.pkl
    if os.path.isdir(model_folder_path) and os.path.exists(model_file_path):
        print(f"Zapisuję model: {model_name}")
        save_model_to_db(model_name, model_file_path, engine)
    else:
        print(f"Pominięto: {model_name}, brak pliku model.pkl")

print("Zakończono zapisywanie modeli do bazy danych.")