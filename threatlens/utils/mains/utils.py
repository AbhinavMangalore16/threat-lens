from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import Logging 

import yaml
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