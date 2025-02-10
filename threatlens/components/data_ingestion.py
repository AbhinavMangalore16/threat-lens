from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logging
from threatlens.entity.config_entity import TrainingPipelineConfig
from threatlens.entity.config_entity import DataIngestionConfig

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

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e: 
            raise ThreatLensException(e, sys)
    def export_df(self):
        try: 
            database_name = self.data_ingestion_config.database
            collection_name = self.data_ingestion_config.collection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collections = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collections.find()))
            if "_id" in df.columns.to_list():
                df.drop("_id", axis=1, inplace=True)
            df.replace({"nan":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise ThreatLensException(e, sys)    
    def init_data_ingestion(self):
        try:
            df = self.export_df()
        except Exception as e:
            raise ThreatLensException(e, sys)