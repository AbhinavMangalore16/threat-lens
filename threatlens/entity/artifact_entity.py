from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

@dataclass 
class DataValidationArtifact:
    is_valid: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_file_path: str

@dataclass
class DataTransformArtifact:
    transform_train_file_path: str
    transform_test_file_path: str
    transform_object_file_path: str

@dataclass
class TrainingMetricArtifact:
    f1_score: float
    precision_score:float
    recall_score: float
    accuracy_score: float

@dataclass
class ModelTrainingArtifact:
    trained_model_file_path : str
    training_metric_artifact: TrainingMetricArtifact
    testing_metric_artifact: TrainingMetricArtifact