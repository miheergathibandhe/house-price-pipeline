import pandas as pd
import numpy as np
import os
import joblib
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__),'..','database'))
from db_connection import get_connection

def predict(test_df):
    print("Loading model...")
    model_path = os.path.join("models","model.pkl")
    model = joblib.load(model_path)

    if 'SalePrice' in test_df.columns:
        test_df = test_df.drop('SalePrice',axis=1)
    print("Making predictions...")
    predictions = model.predict(test_df)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM model_versions")
    model_version_id = cursor.fetchone()[0]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for pred in predictions:
        cursor.execute("""
                        INSERT INTO predictions (model_version_id, predicted_price, timestamp)
                        VALUES (?,?,?)
        """, (model_version_id,round(float(pred),2),timestamp))

    conn.commit()
    conn.close()
    print(f"{len(predictions)} Predictions saved to database.")

    return predictions

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__),'..','ingestion'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'..','transformation'))
    from load_data import load_data
    from clean import clean_data

    train_path = os.path.join("data","raw","train.csv")
    test_path = os.path.join("data","raw","test.csv")

    train_df, test_df = load_data(train_path, test_path)
    train_df, test_df = clean_data(train_df, test_df)
    predictions = predict(test_df)
    print(f"Sample Predictions: {predictions[:5]}")