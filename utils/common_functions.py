#create a function for reading YMAL files, because you are going to read the YAML file at various steps, at data ingestions at data processing
import pandas as pd
import os
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file is not in the given path")
        with open(file_path,'r') as ymal_file:
            config = yaml.safe_load(ymal_file)
            logger.info("Succesfully read the YAML file")
            return config
    except Exception as e:
        logger.error("Error reading while YAML file")
        raise CustomException('Failed to read YAML file', e)
    

def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(F"Error loading data {e}")
        raise CustomException("Failed to load data", e)