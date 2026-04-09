import numpy as np
import pandas as pd 
import os 
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
from datetime import datetime
import sys
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..','database'))
from db_connection import get_connection

def train_model(train_df):
    print("training model...")
    x = train_df.drop(columns='SalePrice', axis=1)
    y = train_df['SalePrice']

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"RMSE: {rmse}")
    print(f"R2 score: {r2}")

    os.makedirs("models",exist_ok=True)
    model_path = os.path.join("models","model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO model_versions (timestamp, model_name,rmse, r2, params)
                   VALUES (?,?,?,?,?)""",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "RandomForestRegressor",
                    round(rmse,2), 
                    round(r2,4),
                    json.dumps({"n_estimators": 100, "random_state": 42})
                    ))
    conn.commit()
    conn.close()
    print("Model version logged to database.")

    return model, x_test, y_test

if __name__ =="__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), '..','ingestion'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'..','transformation'))
    from load_data import load_data
    from clean import clean_data

    train_path = os.path.join("data","raw","train.csv")
    test_path = os.path.join("data","raw","test.csv")

    train_df, test_df = load_data(train_path,test_path)
    train_df, test_df = clean_data(train_df,test_df)
    model, x_test, y_test = train_model(train_df)