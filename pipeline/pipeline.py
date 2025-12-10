from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTrainer
from  utils.common import read_yaml, load_data
from config.paths_config import *


if __name__=="__main__":
    data_ingest = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingest.run()
    processor = DataPreprocessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.run_process()
    trainer = ModelTrainer(PROCESSED_TRAIN_PATH,PROCESSED_TEST_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
    