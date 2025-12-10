import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import sys

logger = get_logger(__name__)

class DataPreprocessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess_data(self,df):
        try:
            logger.info("Starting data process ...")
            logger.info("Dropping the columns...")
            df.drop(columns=['Unnamed: 0','Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)
            cat_cols = self.config["data_processing"]["cat_columns"]
            num_cols = self.config["data_processing"]["num_columns"]

            logger.info("aaplying label encoding")
            le = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = le.fit_transform(df[col])
                mappings[col] = {label:value for label,value in zip(le.classes_,le.transform(le.classes_))}
            logger.info(f"Label mappings are:={mappings}")

            logger.info("Transforming the skewed features...")
            for col in num_cols:
                if df[col].skew() > self.config["data_processing"]["skewness_threshold"]:
                    df[col] = np.log1p(df[col])
            return df
        except Exception as e:
            logger.error("Error during preprocess step..",e)
            raise CustomException("Error while Preprocess data",e)
    def handle_imbalance_data(self,df):
        try:
            logger.info("Handling imbalance data...")
            X = df.drop(columns=["booking_status"])
            y = df.booking_status
            smote = SMOTE(random_state=42)
            x_res, y_res = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(x_res,columns=X.columns)
            balanced_df['booking_status'] = y_res
            logger.info("Data balanced successfully..")
            return balanced_df
        except Exception as e:
            logger.error("Error during handling imbalanced data step..",e)
            raise CustomException("Error while balancing data",e)
        
    def feature_selection_process(self,df):
        try:
            logger.info("Feature selection started....")
            X = df.iloc[:,:-1]
            y = df.iloc[:,-1]
            rf = RandomForestClassifier(random_state=42)
            rf.fit(X,y)
            feature_importance = rf.feature_importances_
            feature_importance_df = pd.DataFrame({"features":X.columns,"importance":feature_importance})
            top_imp_feature_df = feature_importance_df.sort_values(by='importance',ascending=False)
            top_10_features = top_imp_feature_df.features.head(self.config["data_processing"]["select_number_of_feature"]).values
            top_10_df = df[top_10_features.tolist()+ ['booking_status']]
            logger.info("Feture selection completed")
            logger.info(f"Top 10 features:{top_10_df.columns}")
            return top_10_df

        except Exception as e:
            logger.error("Error during feature selection step step..",e)
            raise CustomException("Error while feature selection data",e)  
    
    def save_data(self,df,file_path):
        try:
            logger.info("Saving our data in processed folder..")
            df.to_csv(file_path,index = False)
            logger.info(f"Data Saved to {file_path}")
        except Exception as e:
            logger.error("Error during saving processed data step..",e)
            raise CustomException("Error while processed data",e) 
    def run_process(self):
        try:
            logger.info("Loading the data from Raw directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            train_df = self.handle_imbalance_data(train_df)
            train_df = self.feature_selection_process(train_df)
            test_df = test_df[train_df.columns]
            self.save_data(train_df,PROCESSED_TRAIN_PATH)
            self.save_data(test_df,PROCESSED_TEST_PATH)

            logger.info("data processing completed")
        except Exception as e:
            logger.error("Error during run process step saving processed data step..",e)
            raise CustomException("Error while run processed data",e) 
        
if __name__=="__main__":
    processor = DataPreprocessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.run_process()
    





        