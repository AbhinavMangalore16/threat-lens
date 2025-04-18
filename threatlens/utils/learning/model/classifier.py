from threatlens.exception.exception import ThreatLensException 
from threatlens.logging.logger import logger
from threatlens.constants.training_pipeline import MODEL_FOLDER_NAME, MODEL_FILE_NAME

import os
import sys
import logging

class ThreatLensModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise ThreatLensException(e, sys)
        
    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_preds = self.model.predict(X_transformed)
            return y_preds
        except Exception as e:
            raise ThreatLensException(e, sys)