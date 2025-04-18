from threatlens.constants.training_pipeline import TARGET_COLUMN
from threatlens.constants.training_pipeline import DATA_TRANSFORM_IMPUTER_PARAMETERS
from threatlens.entity.artifact_entity import DataTransformArtifact, DataValidationArtifact
from threatlens.entity.config_entity import DataTransformationConfig
from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger
from threatlens.utils.mains.utils import read_yaml, write_yaml, save_numpy, save_pickle


import os
import sys
import logging 
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


class DataTransformation:
    def __init__(self, data_validation_artifact: DataTransformArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataTransformArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config   
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
        
    def get_transform_pipeline(cls) -> Pipeline:
        logging.info("Creating transformation pipeline pickle")
        print("Creating transformation pipeline pickle")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORM_IMPUTER_PARAMETERS)
            prepro_imputer = Pipeline(steps=[("imputer", imputer)])
            return prepro_imputer
        except Exception as e:
            raise ThreatLensException(e, sys)

    def init_data_transform(self) -> DataTransformArtifact:
        try:
            logging.info("Starting data transformation")
            print("Starting data transformation")
            df_train = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            df_test = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_train_df = df_train.drop(columns=[TARGET_COLUMN], axis = 1)
            target_train_df = df_train[TARGET_COLUMN]
            input_test_df = df_test.drop(columns=[TARGET_COLUMN], axis = 1)
            target_test_df = df_test[TARGET_COLUMN]

            preprocessor = self.get_transform_pipeline()
            preprocessor_obj = preprocessor.fit(input_train_df)
            transform_input_train_df = preprocessor_obj.transform(input_train_df)
            transform_test_input_df = preprocessor_obj.transform(input_test_df)

            train_arr = np.c_[transform_input_train_df, np.array(target_train_df)]
            test_arr = np.c_[transform_test_input_df, np.array(target_test_df)]
            logging.info("Transformation completed successfully")
            print("Transformation completed successfully")
            save_pickle(file_path=self.data_transformation_config.transform_object_file_path, data=preprocessor_obj)
            save_numpy(file_path=self.data_transformation_config.transform_train_file_path, array=train_arr)
            save_numpy(file_path=self.data_transformation_config.transform_test_file_path, array=test_arr)

            save_pickle("production/preprocessor.pkl", preprocessor_obj)

            data_transform_artifact = DataTransformArtifact(
                transform_object_file_path=self.data_transformation_config.transform_object_file_path,
                transform_train_file_path=self.data_transformation_config.transform_train_file_path,
                transform_test_file_path=self.data_transformation_config.transform_test_file_path
            )
            return data_transform_artifact

        except Exception as e:
            raise ThreatLensException(e, sys)