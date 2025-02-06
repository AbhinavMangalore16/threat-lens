import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

import pandas as pd
import numpy as np
import pymongo
import json
from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger

import certifi

load_dotenv()
CA = certifi.where()
MONGO_USERNAME = quote_plus(os.getenv("MONGO_USERNAME"))
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
if not MONGO_USERNAME or not MONGO_PASSWORD:
    raise ValueError("MongoDB credentials are not set in the .env file.")


uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.ys1q0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class Extract():
    def __init__(self):
        try: 
            pass
        except Exception as e:
            raise ThreatLensException(e, sys)
    def data_conversion(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            jsonified = list(json.loads(data.T.to_json()).values())
            return jsonified
        except Exception as e:
            raise ThreatLensException(e, sys)
    def mongo_db_push(self,database, records, collection):
        try: 
            self.database =database
            self.records = records
            self.collection = collection
            self.mongo_client = pymongo.MongoClient(uri)
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
            logger.info(f"Data pushed to {collection} collection in {database} database")
            return len(self.records)
        except Exception as e:
            raise ThreatLensException(e,sys)

File_path = "data/raw/phishing.csv"
Database = "ThreatLens"
Collection = "PhishingNetworkData"
extract = Extract()
data = extract.data_conversion(file_path=File_path)
recs = extract.mongo_db_push(database=Database, records=data, collection=Collection)
logger.info(f"Number of records pushed: {recs}")
