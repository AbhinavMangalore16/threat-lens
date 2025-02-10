from threatlens.components.data_ingestion import DataIngestion
from threatlens.logging.logger import logging
from threatlens.exception.exception import ThreatLensException
from threatlens.entity.config_entity import TrainingPipelineConfig
from threatlens.entity.config_entity import DataIngestionConfig

import sys

if __name__ == '__main__':
    try: 
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("")


    except Exception as e:
        raise ThreatLensException(e, sys) 