import os
import pandas as pd
import joblib
from src.logger import get_logger
from sklearn.model_selection import RandomizedSearchCV
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score,recall_score,precision_score, f1_score
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from scipy.stats import randint
from utils.common import load_data, read_yaml
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTrainer:

    def __init__(self, train_path, test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.params_dist = lgbm_params
        self.random_search_params = random_search_params
       
    
    def load_and_split_data(self):
        try:
            logger.info(f"Loading Data From {self.train_path}")
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)
            logger.info("Data Loaded successfully..")

            x_train = train_data.drop(columns=["booking_status"])
            y_train = train_data['booking_status']
            x_test = test_data.drop(columns=['booking_status'])
            y_test = test_data['booking_status']
            logger.info("Data splitted and loaded successfully..")

            return x_train,y_train,x_test,y_test
        
        except Exception as e:
            logger.error("Error while loading the data")
            raise CustomException("Error while loading and splitting",e)
        
    def train_model(self,x_train,y_train):
        try:
            logger.info("Training started...")
            lgbm = LGBMClassifier(random_state=self.random_search_params['random_state'])
            random_cv = RandomizedSearchCV(
                                            estimator=lgbm,
                                            param_distributions=self.params_dist,
                                            n_iter=self.random_search_params["n_iter"],
                                            cv = self.random_search_params["cv"],
                                            n_jobs = -self.random_search_params["n_jobs"],
                                            verbose = self.random_search_params["verbose"],
                                            random_state = self.random_search_params["random_state"],
                                            scoring = self.random_search_params["scoring"]
                                           )
            
            random_cv.fit(x_train,y_train)
            logger.info("Model training and hyperparameter tuning completed....")
            best_params = random_cv.best_params_
            best_model = random_cv.best_estimator_

            logger.info(f"Best Parameters:{best_params}")
            return best_model
        except Exception as e:
            logger.error("Error while model taining....")
            raise CustomException("Error while training and hyperparameter tuning",e)
            
    def evaluate_model(self,model,x_test,y_test):
        try:
            logger.info("Evaluation is started....")
            y_pred = model.predict(x_test)
            acc_score = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy:{acc_score}")
            logger.info(f"precision:{precision}")
            logger.info(f"recall:{recall}")
            logger.info(f"f1 Score:{f1}")

            return {"accuracy":acc_score,
                    "precision":precision,
                    "recall":recall,
                    "fi_score":f1}
        except Exception as e:
            logger.error("Error while evaluating model....")
            raise CustomException("Error while evaluating lgbm",e)
    
    def save_model(self,model):
        try:
            logger.info("Model saving started...")
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            logger.info("Saving..")
            joblib.dump(model,self.model_output_path)
            logger.info(f"Model Saved at {self.model_output_path}")
        except Exception as e:
            logger.error("Error while saving model....")
            raise CustomException("Error while saving lgbm",e)

    def run(self):
        try:
            logger.info("Starting our model training pipline..")
            with mlflow.start_run():
                logger.info("Starting mlflow Experimentation....")
                logger.info("Logging the data set to mlflow for each experiment tracking")
                mlflow.log_artifact(self.train_path,artifact_path="datasets")
                mlflow.log_artifact(self.test_path,artifact_path='datasets')
                x_train,y_train,x_test,y_test = self.load_and_split_data()
                best_model = self.train_model(x_train,y_train)
                metrics = self.evaluate_model(best_model,x_test,y_test)
                self.save_model(best_model)
                logger.info("Logging the model in mlflow for tracking")
                mlflow.log_artifact(self.model_output_path,artifact_path="models")
                logger.info("Logging best params of models")
                mlflow.log_params(best_model.get_params())
                logger.info("Logging the metrics of models in mlflow")
                mlflow.log_metrics(metrics=metrics)

                

                logger.info(f"Model training successfully completed")
        except Exception as e:
            logger.error("Error while training pipeline....")
            raise CustomException("Error while training pipeline",e)
    
if __name__=="__main__":
    trainer = ModelTrainer(PROCESSED_TRAIN_PATH,PROCESSED_TEST_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
