import sys
from threatlens.logging import logger
class ThreatLensException(Exception):
    def __init__(self, error_msg, error_details:sys):
        self.error_msg = error_msg
        i,j, exec_info = error_details.exc_info()
        self.lineno = exec_info.tb_lineno
        self.file_name = exec_info.tb_frame.f_code.co_filename
    
    def __str__(self):
        return f"Error: {self.error_msg} at line {self.lineno} in file {self.file_name}"
