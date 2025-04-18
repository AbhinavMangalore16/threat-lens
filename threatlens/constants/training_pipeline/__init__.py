import os 
import sys 
import numpy as np
import pandas as pd

TARGET_COLUMN :str= "CLASS_LABEL"
PIPELINE_NAME :str= "threat_lens"
ARTIFACT_DIR :str= "artifacts"
FILE_NAME :str= "phishing.csv"

TRAIN_FILE_NAME :str= "train_data.csv"
TEST_FILE_NAME :str= "test_data.csv"
FILE_SCHEMA_PATH :str= os.path.join("schema", "data_schema.yaml")
MODEL_FOLDER_NAME :str=os.path.join("models_phishing")

"""
====== Data Ingestion constants ======

"""

DATA_INGESTION_COLLECTION :str= "PhishingNetworkData"
DATA_INGESTION_DB :str= "ThreatLens"
DATA_INGESTION_DIR_NAME :str= "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str= "feature_store"
DATA_INGESTION_INGESTED_DIR :str= "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.25



"""
====== Data Validation constants ======

"""

DATA_VALIDATION_DIR_NAME :str= "data_validation"
DATA_VALIDATION_VALID_DIR :str= "valid"
DATA_VALIDATION_INVALID_DIR :str= "invalid"
DATA_VALIDATION_DRIFT_DIR :str= "drift"
DATA_VALIDAITION_DRIFT_FILE :str= "drift.yaml"

"""
====== Data Transformation constants ======

"""

DATA_TRANSFORM_DIR_NAME :str= "data_transform"
DATA_TRANSFORM_TRANSFORMED_DATA_DIR :str= "transformed_data"
DATA_TRANSFORM_TRANSFORMED_OBJECT_DIR :str= "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME :str= "preprocessor.pkl"
DATA_TRANSFORM_IMPUTER_PARAMETERS :dict= {
    "missing_values": np.nan,
    "n_neighbors": 5,
    "weights": "uniform",
}

"""
====== Model Training constants ======

"""
MODEL_TRAINING_DIR_NAME :str= "model_training"
MODEL_TRAINED_DIR :str= "model_trained"
MODEL_FILE_NAME :str= "phish_model.pkl"
MODEL_TRAINING_REPORT_DIR :str= "training_report"
MODEL_TRAINING_REPORT_FILE_NAME :str= "phish_model_report.yaml"
MODEL_TRAINING_ACCURACY_THRESHOLD :float= 0.7
MODEL_TRAINING_OVERFITTING_UNDERFITTING_THRESHOLD :float = 0.05
