from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd
import numpy as np
from pandas import DataFrame
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.sensor_data = SensorData()
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            logging.info(f"Data ingestion configuration")
           
        except Exception as e:
            raise SensorException(e, sys)
        
        
        
    def load_data_into_feature_store(self):
        """ export mongoDB collection record as a dataframe  into feature
        """
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            dataframe = self.sensor_data.export_collection_as_df(collection_name=self.data_ingestion_config.collection_name)
            print(dataframe.info())
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            #creating folder for storing file mongo data
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            
            return dataframe
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """

        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class")
            

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True)
            

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True)
            

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise SensorData(e,sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            
            dataframe:DataFrame = self.load_data_into_feature_store()
            logging.info(f"Dataframe shape: {dataframe.shape}")
            
            dataframe.replace({"na": np.nan}, inplace=True)
            logging.info(f"Replacing na values with np.nan")
            
            dataframe= dataframe.drop(self._schema_config["drop_columns"], axis=1)
            logging.info(f"Dropping drop_columns {self._schema_config['drop_columns']}")
            
            # train_df, test_df = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            # logging.info(f"Splitting data into train and test {train_df.shape, test_df.shape}")
            
            
            # logging.info(f"Creating dataset directory")
            # dataset_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            # os.makedirs(dataset_dir, exist_ok=True)
            # logging.info(f"Dataset directory created: {dataset_dir}")
            
            # logging.info(f"Saving train and test data to dataset directory")
            # train_df.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            # test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            # logging.info(f"train and test files are created and saved")
            
            logging.info(f"Splitting data into train and test")
            self.split_data_as_train_test(dataframe=dataframe)
            
            logging.info(f"Preparing data ingestion artifact")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"data_ingestion_artifact is created: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)



if __name__ == "__main__":
    
    obj= DataIngestion()
    

