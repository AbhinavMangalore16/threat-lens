from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logging
from threatlens.entity.config_entity import DataIngestionConfig
from threatlens.entity.artifact_entity import DataIngestionArtifact


from dotenv import load_dotenv
import sys
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import List, Dict

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
if not MONGO_DB_URI:
    raise ThreatLensException("MONGO_DB_URI not found in environment variables.", sys)

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
        except Exception as e: 
            raise ThreatLensException(e, sys)
    def export_df(self):
        try: 
            logging.info("Exporting data from MongoDB to DataFrame")
            print("Exporting data from MongoDB to DataFrame")
            database_name = self.data_ingestion_config.database
            collection_name = self.data_ingestion_config.collection
            collections = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collections.find()))
            if "_id" in df.columns.to_list():
                df.drop("_id", axis=1, inplace=True)
            df.replace({"nan":np.nan}, inplace=True)
            logging.info("Data exported successfully")
            print("Data exported successfully")
            return df
        except Exception as e:
            raise ThreatLensException(e, sys) 
    def export_feature_store(self, df: pd.DataFrame):
        try:
            logging.info("Exporting data to feature store")
            print("Exporting data to feature store")
            feature_store_path = self.data_ingestion_config.feature_store_dir
            directory_feature_store = os.path.dirname(feature_store_path)
            os.makedirs(directory_feature_store, exist_ok=True)
            df.to_csv(feature_store_path, index=False, header=True)
            logging.info(f"Data exported to feature store at {feature_store_path}")
            print(f"Data exported to feature store at {feature_store_path}")
            return df
        except Exception as e:
            raise ThreatLensException(e, sys)
    def train_test_split_section(self, df: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets")
            print("Splitting data into train and test sets")
            df_train, df_test = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train and Test data split successful")
            print("Train and Test data split successful")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file)
            os.makedirs(dir_path, exist_ok=True)
            df_train.to_csv(self.data_ingestion_config.training_file, index=False, header=True)
            print(f"Train data saved at {self.data_ingestion_config.training_file}")
            logging.info(f"Train data saved at {self.data_ingestion_config.training_file}")
            df_test.to_csv(self.data_ingestion_config.testing_file, index=False, header=True)
            logging.info(f"Test data saved at {self.data_ingestion_config.testing_file}")
            print(f"Test data saved at {self.data_ingestion_config.testing_file}")
        except Exception as e:
            raise ThreatLensException(e, sys)
    def init_data_ingestion(self)-> DataIngestionArtifact:
        try:
            df = self.export_df()
            df = self.export_feature_store(df)
            self.train_test_split_section(df)
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file, test_file_path=self.data_ingestion_config.testing_file)
            return data_ingestion_artifact
        except Exception as e:
            raise ThreatLensException(e, sys)