
import os
import sys 
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


sys.path.append(os.path.join("src","ingestion"))
sys.path.append(os.path.join("src","transformation"))
sys.path.append(os.path.join("src","database"))
sys.path.append(os.path.join("src","models"))
sys.path.append(os.path.join("src","predictions"))

from load_data import load_data
from clean import clean_data
from db_connection import init_db, save_clean_data
from train import train_model
from predict import predict

def main():
    print("Pipeline starting...")
    logger.info("Pipeline started.")

    logger.info("Step 1- loading data...")
    train_path = os.path.join('data','raw','train.csv')
    test_path = os.path.join('data','raw','test.csv')
    train_df, test_df = load_data(train_path, test_path)

    logger.info("Step 2- cleaning data...")
    train_df, test_df = clean_data(train_df, test_df)

    logger.info("Step 3- initializing model...")
    init_db()

    logger.info("Step 4- saving cleaned data to database...")
    save_clean_data(train_df)

    logger.info("Step 5- training model...")
    train_model(train_df)

    logger.info("Step 6- making predictions...")
    predictions = predict(test_df)

    logger.info("Pipeline completed successfully")
    logger.info(f"Total Predictions: {len(predictions)}")

if __name__ == "__main__":
    main()