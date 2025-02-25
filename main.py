from threatlens.components.data_ingestion import DataIngestion
from threatlens.logging.logger import logging
from threatlens.exception.exception import ThreatLensException
from threatlens.entity.config_entity import TrainingPipelineConfig
from threatlens.entity.config_entity import DataIngestionConfig

import sys

if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiating Data Ingestion..")
        data_ingestion_artifact = data_ingestion.init_data_ingestion()
        print(data_ingestion_artifact)
    except ThreatLensException as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    sys.exit(0)
