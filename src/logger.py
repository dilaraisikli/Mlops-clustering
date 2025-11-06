import logging
import os #for creating diracties
from datetime import datetime
#we will store all our logs in a directory like we we will name the direcorty as logs, we need os libary for that

LOGS_DIR = "logs"  #directory (dizin) name created
os.makedirs(LOGS_DIR, exist_ok = True) 

LOGS_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
# for each log, we will save it with date time information

logging.basicConfig( #config = yapilandirma
    filename = LOGS_FILE,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
    #there are a lot of levels but now we use only 3 leves info , warning and error
)
def get_logger(name):
   logger = logging.getLogger(name)
   logger.setLevel(logging.INFO) 
   return logger

