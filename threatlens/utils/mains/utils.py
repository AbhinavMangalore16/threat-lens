from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger


import yaml
import logging
import os
import sys
import numpy as np
import pickle
import dill

def read_yaml(file_path: str):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise ThreatLensException(e, sys)
    
def write_yaml(file_path: str,  content: object, replace: bool = False)-> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            yaml.dump(content, f)
    except Exception as e:
        raise ThreatLensException(e, sys)
    
def save_numpy(file_path: str, array:np.array) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            np.save(f, array)
    except Exception as e:  
        raise ThreatLensException(e, sys)
    
def load_numpy(file_path: str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "rb") as f:
            return np.load(f)
    except Exception as e:
        raise ThreatLensException(e, sys)
    
def save_pickle(file_path: str, data: object) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        raise ThreatLensException(e, sys)
    
def load_pickle(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise ThreatLensException(e, sys)