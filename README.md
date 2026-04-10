# house-price-pipeline

An end-to-end Machine Learning + Data Engineering pipeline that predicts house prices using the Kaggle House Prices dataset.

## Architecture

## Project Structure
```
house-price-pipeline/
├── data/
│   ├── raw/              # Original CSV files
│   └── processed/        # Processed data
├── src/
│   ├── ingestion/        # load_data.py
│   ├── transformation/   # clean.py
│   ├── database/         # db_connection.py, schema.sql
│   ├── models/           # train.py
│   └── predictions/      # predict.py
├── main.py               # Pipeline entry point
├── requirements.txt
└── README.md
```

##Tech Stack
- Python, pandas, Numpy
- Scikit-learn (Random forest)
- SQLAlchemy = sqlite
- Joblib

## Pipeline Steps
1. **Ingestion** - Load raw CSV data
2. **Transformation** - Handle missing values, encode categories
3. **Database** - Store clean data in SQLite
4. **Training** - Train Random forest, log model version to db
5. **Prediction** - Generate predictions, store in db

## Model Performance
- RMSE: 41,245
- R2: 0.7782

## How to run
''' bash
pip install -r requirements.txt
python main.py
'''

## Key Features
- Modular pipeline scripts
- SQL database layer
- Model versioning table
- Predictions stored in database
- End to end automation via main.py