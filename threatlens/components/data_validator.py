from threatlens.entity.config_entity import DataIngestionConfig
from threatlens.entity.config_entity import DataValidationConfig
from threatlens.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from threatlens.constants.training_pipeline import FILE_SCHEMA_PATH
from threatlens.logging.logger import logger
from threatlens.utils.mains.utils import read_yaml, write_yaml
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
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from {file_path}")
            print(f"Reading data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise ThreatLensException(e, sys)

    def validate_data_schema(self, df: pd.DataFrame) -> bool:
        try:
            logging.info("Validating data schema")
            print("Validating data schema")
            schema_columns = len(self._schema_config["columns"])
            incoming_columns = len(df.columns)
            logging.info(f"Schema columns: {schema_columns}")
            logging.info(f"Incoming Dataframe columns: {incoming_columns}")
            print("Schema columns: ", schema_columns)
            print("Incoming Dataframe columns: ", incoming_columns)
            if incoming_columns == schema_columns:
                logging.info("Incoming Dataframe columns match the schema.")
                print("Incoming Dataframe columns match the schema.")
                return True
            return False
        except Exception as e:
            raise ThreatLensException(e, sys)

    def validate_numeric_schema(self, df: pd.DataFrame) -> bool:
        try:
            logging.info("Validating numeric schema")
            print("Validating numeric schema")
            numeric_columns = self._schema_config.get("numeric", [])
            missing_cols = [col for col in numeric_columns if col not in df.columns]
            if missing_cols:
                logging.error(f"Missing numeric columns: {missing_cols}")
                print(f"Missing numeric columns: {missing_cols}")
                return False
            logging.info("All required numeric columns present.")
            print("All required numeric columns present.")
            return True
        except Exception as e:
            raise ThreatLensException(e, sys)

    def validate_data_drift(self, main_df, hypo_df, threshold_val=0.05) -> bool:
        try:
            logging.info("Validating data drift")
            print("Validating data drift")
            status = True
            drift_report = {}
            common_columns = list(set(main_df.columns) & set(hypo_df.columns))
            
            for col in common_columns:
                dp1 = main_df[col]
                dp2 = hypo_df[col]
                kolmogorov_smirnov_val = ks_2samp(dp1, dp2)
                is_drift = (kolmogorov_smirnov_val.pvalue < threshold_val)
                if is_drift:
                    status = False
                drift_report.update({col: {"is_Drift": bool(is_drift), "p_ks_value": float(kolmogorov_smirnov_val.pvalue)}})
                logging.info(f"Drift report for {col}: {drift_report[col]}")
                print(f"Drift report for {col}: {drift_report[col]}")
            
            drift_report_path = self.data_validation_config.drift_file_path
            drift_dir_path = os.path.dirname(drift_report_path)
            os.makedirs(drift_dir_path, exist_ok=True)
            write_yaml(drift_report_path, drift_report)
            return status
        except Exception as e:
            raise ThreatLensException(e, sys)

    def init_data_valid(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = DataValidator.read_data(train_file_path)
            test_df = DataValidator.read_data(test_file_path)
            
            status1 = self.validate_data_schema(train_df) and self.validate_numeric_schema(train_df)
            status2 = self.validate_data_schema(test_df) and self.validate_numeric_schema(test_df)
            
            if not status1:
                error_msg = f"Schema validation failed. Expected {len(self._schema_config)} columns, but got {len(train_df.columns)} columns."
                print(error_msg)
                logging.error(error_msg)
            if not status2:
                error_msg = f"Schema validation failed. Expected {len(self._schema_config)} columns, but got {len(test_df.columns)} columns."
                print(error_msg)
                logging.error(error_msg)

            drift_status = self.validate_data_drift(train_df, test_df)

            print("Data Drift? || status: ", not drift_status)
            logging.info(f"Data Drift? || status: {not drift_status}")
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Saving valid train and test files")
            print("Saving valid train and test files")
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            data_valid_artifact = DataValidationArtifact(
                is_valid=status1 and status2,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_file_path=self.data_validation_config.drift_file_path
            )
            logging.info("Data validation completed successfully")
            print("Data validation completed successfully")
            return data_valid_artifact
        except Exception as e:
            raise ThreatLensException(e, sys)


