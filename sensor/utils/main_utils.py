#here we write how to share url/data to mongodb
from sensor.logger import logging
import pandas as pd
import numpy as np
import json
from sensor.config import mongo_client
import yaml
import dill
import sys
from sensor.exception import SensorException   
import os


# def dump_csvfile_to_mongodb(filepath:str,
#                             database_name:str,
#                             collection_name:str)->None: #since we dont want to return anythin we jsut want to pass
    
#     try:
        
#         df= pd.read_csv(filepath)
#         df.reset_index(drop=True,inplace=True)
#         json_records=list(json.loads(df.T.to_json()).values())
#         mongo_client[database_name][collection_name].insert_many(json_records)
#         logging.info("Database loaded succesfully")
        
#     except Exception as e:
#         print(e)

def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath,'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise SensorException(e,sys)
    
    
def write_yaml_file(filepath:str, content:object, replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            yaml.dump(content, f)
    except Exception as e:
        raise SensorException(e, sys)
        
        
def save_numpy_array_data(filepath:str, array: np.array):
    
    """Save numpy array data to file
        filepath: location to store the numpy array
        array: numpy array to be saved
    """
    
    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'wb') as f:
            np.save(f, array)
    except Exception as e:
        raise SensorException(e, sys)
        
        
def load_numpy_array_data(filepath:str)->np.array:
    """Load numpy array data from file
        filepath: str location of the file path
        array: numpy array to be saved
    """
    try:
        with open(filepath, 'rb') as f:
            return np.load(f)
    except Exception as e:
        raise SensorException(e, sys)
    
def save_object(filepath:str, obj:object)->None:
    """Save an object to file
        filepath: str location of the file path
        obj: object to be saved
    """
    try:
        logging.info("Saving object using method written in main_utils")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            dill.dump(obj, f)
            
        logging.info("Object saved succesfully and exit from main_utils")
    except Exception as e:
        raise SensorException(e, sys)
    
    
def load_object(file_path:str)->object:
    """Load an object from file
        filepath: str location of the file path
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} does not exist")
        with open(file_path, 'rb') as f:
            return dill.load(f)
    except Exception as e:
        raise SensorException(e, sys)
        