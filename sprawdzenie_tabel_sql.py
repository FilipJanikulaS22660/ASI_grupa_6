import pandas as pd
from sqlalchemy import create_engine, text

# Utwórz połączenie z bazą danych
engine = create_engine('postgresql+psycopg2://kedro_user:password@localhost:5432/kedro_db')

# Funkcja do wylistowania wszystkich tabel w bazie danych
def list_tables(engine):
    query = text("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    """)
    with engine.connect() as connection:
        result = connection.execute(query)
        tables = result.fetchall()
    return [table[0] for table in tables]

# Wylistowanie tabel
tables = list_tables(engine)
print("Tabele w bazie danych:")
for table in tables:
    print(table)