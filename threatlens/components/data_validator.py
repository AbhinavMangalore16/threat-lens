from threatlens.entity.config_entity import DataIngestionConfig
from threatlens.entity.config_entity import DataValidationConfig
from threatlens.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from threatlens.constants.training_pipeline import FILE_SCHEMA_PATH
from threatlens.logging.logger import logger
from threatlens.utils.mains.utils import read_yaml
from threatlens.exception.exception import ThreatLensException

import os
import sys
import logging 
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import ks_2samp


class DataValidator:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(FILE_SCHEMA_PATH)
        except Exception as e:
            raise ThreatLensException(e, sys)
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ThreatLensException(e, sys)
        
    def validate_data_schema(self, df: pd.DataFrame) -> bool:
        try:
            schema_columns = len(self._schema_config)
            incoming_columns = len(df.columns)
            logging.infO(f"Schema columns: {schema_columns}")
            logging.info(f"Incoming Dataframe columns: {incoming_columns}")
            if incoming_columns == schema_columns:
                logging.info("Incoming Dataframe columns match the schema.")
                return True
            return False            
        except Exception as e:
            raise ThreatLensException(e, sys)
    
    def validate_numeric_schema(self, df: pd.DataFrame) -> bool:
        try:
            numeric_columns = self._schema_config.get("numeric", [])
            missing_cols  = [col for col in numeric_columns if col not in df.columns]
            if missing_cols:
                logging.error(f"Missing numeric columns: {missing_cols}")
                return False
            logging.info("All required numeric columns present.")
            return True            
        except Exception as e:
            raise ThreatLensException(e, sys)

    def init_data_valid(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = DataValidator.read_data(train_file_path)
            test_df = DataValidator.read_data(test_file_path)
            status1 = self.validate_data_schema(train_df) and self.validate_numeric_schema(train_df)
            status2 = self.validate_data_schema(test_df) and self.validatie_numeric_schema(test_df)
            if not status1:
                error_msg = f"Schema validation failed. Expected {len(self._schema_config)} columns, but got {len(train_df.columns)} columns."
                logging.error(error_msg)
            if not status2:
                error_msg = f"Schema validation failed. Expected {len(self._schema_config)} columns, but got {len(test_df.columns)} columns."
                logging.error(error_msg)

        except Exception as e:
            raise ThreatLensException(e, sys)

