import pandas as pd
import os

def load_data(train_path, test_path):
    print("Loading data...")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")

    return train_df, test_df

if __name__ == "__main__":
    train_path = os.path.join("data","raw","train.csv")
    test_path = os.path.join("data","raw","test.csv")

    train_df, test_df = load_data(train_path, test_path)
    print(train_df.head())

