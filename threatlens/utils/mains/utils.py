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