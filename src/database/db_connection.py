import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import os

db_path = os.path.join("data","house_prices.db")

def get_engine():
    engine = create_engine(f"sqlite3:///(db_path)")
    return engine

def get_connection():
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = os.path.join("src","database","schema.sql")
    with open(schema_path, "r") as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Database intialized.")

def save_clean_data(train_df):
    print("saving clean data to database...")
    engine = get_engine()

    cols = ['GrLivArea','BedroomAbvGr','FullBath','YearBuilt','OverallQual','SalePrice']
    train_df[cols].to_sql('house_prices', con=engine, if_exists='replace', index= False)

    print("Data saved to database.")

if __name__ == "__main__":
    init_db()