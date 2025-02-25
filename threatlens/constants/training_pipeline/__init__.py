import os 
import sys 
import numpy as np
import pandas as pd

"""
====== Data Ingestion constants ======

"""

DATA_INGESTION_COLLECTION = "PhishingNetworkData"
DATA_INGESTION_DB = "ThreatLens"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.25


TARGET_COLUMN = "CLASS_LABEL"
PIPELINE_NAME = "threat_lens"
ARTIFACT_DIR = "artifacts"
FILE_NAME = "phishing.csv"

TRAIN_FILE_NAME = "train_data.csv"
TEST_FILE_NAME = "test_data.csv"

"""
====== Data Validation constants ======

"""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "valid"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_DIR = "drift"
DATA_VALIDAITION_DRIFT_FILE = "drift.yaml"