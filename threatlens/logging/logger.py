import logging 
import os
from datetime import datetime

LOGGING_FILE  = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

logging_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logging_path, exist_ok=True)

LOGGING_FILE_PATH = os.path.join(logging_path, LOGGING_FILE)


logging.basicConfig(
    filename=LOGGING_FILE_PATH, 
    format='[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger(__name__)