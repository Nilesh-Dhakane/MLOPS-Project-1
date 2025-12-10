import os 
import pandas as pd 
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File is not found in given path")
        with open(file_path,"r") as file:
            config = yaml.safe_load(file)
        return config
        logger.info("Successfully read the yaml file")    
    except Exception as e:
        logger.error("Error while reading the yaml file...")
        raise CustomException("Failed to read yaml file",e)
    
def load_data(file_path):
    try:
        logger.info("Loading data...")
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error("Loading the data",e)
        raise CustomException("Exception while Loading data",e)