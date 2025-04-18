from datetime import datetime 
import os

from threatlens.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%Y%m%d%H%M%S") or datetime.now().strftime("%Y%m%d%H%M%S")
        self.pipeline_name :str= training_pipeline.PIPELINE_NAME
        self.artifact_name :str= training_pipeline.ARTIFACT_DIR
        self.artifact_dir :str= os.path.join(self.artifact_name, self.timestamp)


class DataIngestionConfig:
    def __init__(self,  training_pipeline_config: TrainingPipelineConfig):
        self.collection :str= training_pipeline.DATA_INGESTION_COLLECTION
        self.database :str= training_pipeline.DATA_INGESTION_DB
        self.data_ingestion_dir :str= os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_dir :str= os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        self.training_file :str= os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.testing_file :str= os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio :float= training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir :str= os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_dir :str= os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_dir :str= os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path :str= os.path.join(self.valid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path :str= os.path.join(self.valid_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path :str= os.path.join(self.invalid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path :str= os.path.join(self.invalid_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_file_path :str= os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_DIR, training_pipeline.DATA_VALIDAITION_DRIFT_FILE)

class DataTransformationConfig:
   def __init__(self, training_pipeline_config: TrainingPipelineConfig):
       self.data_transform_dir :str= os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORM_DIR_NAME)
       self.transform_train_file_path :str= os.path.join(self.data_transform_dir, training_pipeline.DATA_TRANSFORM_TRANSFORMED_DATA_DIR,training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
       self.transform_test_file_path :str= os.path.join(self.data_transform_dir, training_pipeline.DATA_TRANSFORM_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))
       self.transform_object_file_path :str= os.path.join(self.data_transform_dir, training_pipeline.DATA_TRANSFORM_TRANSFORMED_OBJECT_DIR, training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_training_dir :str= os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINING_DIR_NAME)
        self.model_trained_file_path :str = os.path.join(self.model_training_dir, training_pipeline.MODEL_TRAINED_DIR, training_pipeline.MODEL_FILE_NAME)
        self.model_training_report :str = os.path.join(self.model_training_dir, training_pipeline.MODEL_TRAINING_REPORT_DIR, training_pipeline.MODEL_TRAINING_REPORT_FILE_NAME)
        self.accuracy_threshold : float = training_pipeline.MODEL_TRAINING_ACCURACY_THRESHOLD
        self.overfitting_underfitting_threshold : float= training_pipeline.MODEL_TRAINING_OVERFITTING_UNDERFITTING_THRESHOLD