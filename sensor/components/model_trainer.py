from sensor.entity.artifact_entity import ModelTrainerArtifact, ClassificationMetricArtifact,DataTransformationArtifact
from sensor.entity.config_entity import ModelTrainerConfig,DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import load_numpy_array_data, load_object, save_object


from xgboost import XGBClassifier
from sklearn.metrics import f1_score, accuracy_score
from sensor.ml.metrics.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import GridSearchCV
import os



class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config: ModelTrainerConfig):
        
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
            
        except Exception as e:
            raise SensorException(e, sys)
        
    def perform_hyper_paramter_tuning(self, x, y):
        """
        perform hyper parameter tuning on model
        """
        try:
            xgb_clf = XGBClassifier(random_state=42)
            param_grid = self.model_trainer_config.hyperparameter_grid

            grid = GridSearchCV(xgb_clf, param_grid, cv=5, verbose=1)
            grid.fit(x, y)

            xgb_clf = grid.best_estimator_

            return xgb_clf

        except Exception as e:
            raise SensorException(e, sys)
        
        
    def train_model(self, x_train, y_train):
        """
        train the model on training data
        """
        try:
            # xgb_clf = self.perform_hyper_paramter_tuning(x_train, y_train)
            xgb_clf= XGBClassifier(random_state=42)
            xgb_clf.fit(x_train, y_train)
        
            return xgb_clf
        
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        """
        initiate model training on train and test data
        """
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("Loading train and test data")
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            logging.info("Splitting dependent and independent variables from train and test data")
            logging.info("Training the model")
            model = self.train_model(x_train, y_train)

            logging.info("Making predictions on training and testing data")
            yhat_train = model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=yhat_train)
            logging.info(f"Prediction for train data: {yhat_train}")
            logging.info(f"Classification train metric: {classification_train_metric}")

            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")

            yhat_test = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=yhat_test)
            logging.info(f"Prediction for train data: {yhat_train}")
            logging.info(f"Classification train metric: {classification_train_metric}")

            # Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)

            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is overfitted or underfitted")

            preprocessor_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            
            sensor_model = SensorModel(preprocessor=preprocessor_obj,model=model)

            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)
    
        

