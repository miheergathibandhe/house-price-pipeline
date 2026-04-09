import pandas as pd
import os
import numpy as np

def clean_data(train_df, test_df):
    print("Cleaning data...")

    threshold = 0.5
    valid_cols = train_df.columns[train_df.isnull().mean() < threshold]

    train_df = train_df[valid_cols].copy()
    test_df = test_df.reindex(columns=valid_cols, fill_value=np.nan).copy()

    target = train_df['SalePrice']
    train_df = train_df.drop('SalePrice',axis=1)

    num_cols = train_df.select_dtypes(include=["int64","float64"]).columns
    for col in num_cols:
        median = train_df[col].median()
        train_df[col] = train_df[col].fillna(median)
        test_df[col] = test_df[col].fillna(median)

    cat_cols = train_df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        mode = train_df[col].mode()[0]
        train_df[col]= train_df[col].fillna(mode)
        test_df[col]= test_df[col].fillna(mode)

    train_df = pd.get_dummies(train_df)
    test_df = pd.get_dummies(test_df)

    train_df, test_df = train_df.align(test_df,join='left',axis=1,fill_value=0)

    print(f"train shape after cleaning: {train_df.shape}")
    print(f"Test shape after cleaning: {test_df.shape}")

    train_df['SalePrice'] = target
    return train_df, test_df

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__),'..','ingestion'))
    from load_data import load_data
    train_path = os.path.join("data","raw","train.csv")
    test_path = os.path.join("data","raw","test.csv")
    train_df, test_df = load_data(train_path, test_path)
    train_df, test_df = clean_data(train_df,test_df)
    print(train_df.head())