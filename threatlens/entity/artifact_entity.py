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