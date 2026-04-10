import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import os

db_path = os.path.join("data","house_prices.db")

def get_engine():
    engine = create_engine(f"sqlite:///(db_path)")
    return engine

def get_connection():
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    print("Initializing database...")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS house_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            GrLivArea REAL,
            BedroomAbvGr REAL,
            FullBath REAL,
            YearBuilt REAL,
            OverallQual REAL,
            SalePrice REAL
        );

        CREATE TABLE IF NOT EXISTS model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            model_name TEXT,
            rmse REAL,
            r2 REAL,
            params TEXT
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_version_id INTEGER,
            predicted_price REAL,
            timestamp TEXT
        );
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def save_clean_data(train_df):
    print("saving clean data to database...")
    engine = get_engine()

    cols = ['GrLivArea','BedroomAbvGr','FullBath','YearBuilt','OverallQual','SalePrice']
    train_df[cols].to_sql('house_prices', con=engine, if_exists='replace', index= False)

    print("Data saved to database.")

if __name__ == "__main__":
    init_db()