from distutils import dir_util  #to read util from util folder
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            # self.data_validation_artifact = DataValidationArtifact()
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            logging.info(f"Data validation configuration")
            
        except Exception as e:
            raise SensorException(e, sys)
        
    def drop_zero_std_column(self,dataframe):
        """It will drop the columns with zero standard deviation
        """
        try:
            zero_std_columns = dataframe.columns[dataframe.std() == 0]
            dataframe.drop(columns=zero_std_columns, inplace=True)
            logging.info(f"Zero standard deviation columns dropped: {zero_std_columns}")
            
        except Exception as e:
            raise SensorException(e, sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """It will validate the number of columns in the dataframe
        """
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            
            if len(dataframe.columns) == number_of_columns:
                return True
            return False

        except Exception as e:
            raise SensorException(e, sys)
        
    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """It will check if the numerical columns exist in the dataframe
        """
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            return numerical_column_present

        except Exception as e:
            raise SensorException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys)
        
    def detect_datasets_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                # is_same_dist = d1.shape == d2.shape
                is_same_dist = ks_2samp(d1, d2)  #ks_2samp is used to check if the two distributions are same or not
                
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
            report.update({column:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
                
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(filepath=drift_report_file_path, content=report)

            return status

        except Exception as e:
            raise SensorException(e, sys)
    
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info(f"Initiating data validation")

            error_message = ""
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading dataframe from train and test files
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            logging.info(f"Train dataframe columns: {train_dataframe.shape},"
                         f"Test dataframe columns: {test_dataframe.shape}")

            # self.drop_zero_std_column(train_dataframe)
            # self.drop_zero_std_column(test_dataframe)

            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}  all columns are not available in train dataframe. \n"
                logging.info(error_message)
                raise Exception(error_message)

            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} numerical columns are not available in train dataset. \n"
                logging.info(error_message)
                raise Exception(error_message)

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} all columns are not available in test dataframe. \n"
                logging.info(error_message)
                raise Exception(error_message)

            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} numerical columns are not available in test dataframe \n"
                logging.info(error_message)
                raise Exception(error_message)
            
            if len(error_message) > 0:
                raise Exception(error_message)

            #chekihn drif in datasets of train and test
            status = self.detect_datasets_drift(base_df=train_dataframe, current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        