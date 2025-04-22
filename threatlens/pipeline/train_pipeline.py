from threatlens.components.data_ingestion import DataIngestion
from threatlens.components.data_transform import DataTransformation
from threatlens.components.data_validator import DataValidator
from threatlens.components.model_training import ModelTraining

from threatlens.logging.logger import logger
from threatlens.exception.exception import ThreatLensException
from threatlens.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainingConfig, TrainingPipelineConfig
from threatlens.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformArtifact, ModelTrainingArtifact

import os
import sys
import logging 

class TrainPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise ThreatLensException(e, sys) from e

    def initialize_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("STAGE I P: Initiating Data Ingestion..")
            print("STAGE I P: Initiating Data Ingestion..")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.init_data_ingestion()
            logging.info("STAGE I E: Data Ingestion completed successfully..")
            print("STAGE I E: Data Ingestion completed successfully..")
            logging.info("Output DI artifact: %s", data_ingestion_artifact)
            print("Output DI artifact: %s", data_ingestion_artifact)
            return data_ingestion_artifact
        except Exception as e:
            raise ThreatLensException(e, sys) from e
    
    def initialize_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("STAGE II P: Initiating Data Validation..")
            print("STAGE II P: Initiating Data Validation..")   
            data_validation = DataValidator(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)     
            data_validation_artifact = data_validation.init_data_valid()
            logging.info("STAGE II E: Data Validation completed successfully..")
            print("STAGE II E: Data Validation completed successfully..")
            logging.info("Output DV artifact: %s", data_validation_artifact) 
            print("Output DV artifact: %s", data_validation_artifact)
            return data_validation_artifact
        except Exception as e:
            raise ThreatLensException(e, sys) from e
    
    def initialize_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformArtifact:
        try:
            logging.info("STAGE III P: Initiating Data Transformation..")
            print("STAGE III P: Initiating Data Transformation..")
            self.data_transforma_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=self.data_transforma_config)
            data_transformation_artifact = data_transformation.init_data_transform()
            logging.info("STAGE III E: Data Transformation completed successfully..")
            print("STAGE III E: Data Transformation completed successfully..")
            logging.info("Output DT artifact: %s", data_transformation_artifact)
            return data_transformation_artifact
        except Exception as e:
            raise ThreatLensException(e, sys) from e
        
    def initialize_model_training(self, data_transform_artifact: DataTransformArtifact) -> ModelTrainingArtifact:
        try: 
            logging.info("STAGE IV P: Initiating Model Training..")
            print("STAGE IV P: Initiating Model Training..")
            self.model_training_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
            model_training = ModelTraining(data_transform_artifact=data_transform_artifact, model_training_config=self.model_training_config)
            model_training_artifact = model_training.init_model_training()
            logging.info("STAGE IV E: Model Training completed successfully..")
            print("STAGE IV E: Model Training completed successfully..")
            logging.info("Output MT artifact: %s", model_training_artifact)
            print("Output MT artifact: %s", model_training_artifact)
            return model_training_artifact
        except Exception as e:
            raise ThreatLensException(e, sys) from e
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.initialize_data_ingestion()
            data_validation_artifact = self.initialize_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transform_artifact = self.initialize_data_transformation(data_validation_artifact=data_validation_artifact)
            model_training_artifact = self.initialize_model_training(data_transform_artifact=data_transform_artifact)
            logging.info("Threatlens Training Pipeline completed successfully.")
            print("Threatlens Training Pipeline completed successfully.")
            return model_training_artifact
        except Exception as e:
            raise ThreatLensException(e, sys) from e


