import sys
import traceback
from threatlens.logging import logger
class ThreatLensException(Exception):
    def __init__(self, error_msg, error_details: sys):
        self.error_msg = error_msg
        exc_type, exc_value, exc_traceback = error_details.exc_info()  

        # Extract line number and filename
        self.lineno = None
        self.file_name = None

        if exc_traceback:
            last_tb = traceback.extract_tb(exc_traceback)[-1]  
            self.lineno = last_tb.lineno
            self.file_name = last_tb.filename

    def __str__(self):
        return f"Error: {self.error_msg} at line {self.lineno} in file {self.file_name}"
