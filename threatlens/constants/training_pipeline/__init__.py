import os 
import sys 
import numpy as np
import pandas as pd


DATA_INGESTION_COLLECTION = "PhishingNetworkData"
DATA_INGESTION_DB = "ThreatLens"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.25