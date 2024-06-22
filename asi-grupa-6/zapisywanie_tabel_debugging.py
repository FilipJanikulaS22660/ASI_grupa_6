import pandas as pd
from sqlalchemy import create_engine

# Wczytaj dane z pliku Excel
df = pd.read_excel("data/01_raw/heart-disease.xlsx")

# Utwórz połączenie z bazą danych
engine = create_engine('postgresql://kedro_user:password@localhost:5432/kedro_db')

# Zapisz dane do tabeli health_data
df.to_sql('health_data', engine, if_exists='replace', index=False)