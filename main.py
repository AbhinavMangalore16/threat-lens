from threatlens.components.data_ingestion import DataIngestion
from threatlens.components.data_validator import DataValidator
from threatlens.logging.logger import logging
from threatlens.exception.exception import ThreatLensException
from threatlens.entity.config_entity import TrainingPipelineConfig
from threatlens.entity.config_entity import DataIngestionConfig, DataValidationConfig

import sys

if __name__ == '__main__':


    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("STAGE I P: Initiating Data Ingestion..")
        print("STAGE I P: Initiating Data Ingestion..")
        data_ingestion_artifact = data_ingestion.init_data_ingestion()
        logging.info("STAGE I E: Data Ingestion completed succesfully..")
        print("STAGE I E: Data Ingestion completed succesfully..")
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidator(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)      
        logging.info("STAGE II P: Initiating Data Validation..")
        data_validation_artifact = data_validation.init_data_valid()
        logging.info("STAGE II E: Data Validation completed successfully..")
        logging.info("Partial Pipeline completed successfully.")
        
    except ThreatLensException as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    sys.exit(0)
