from sensor.exception import SensorException,sys
from sensor.logger import logging
from sensor.utils import dump_csvfile_to_mongodb
import pandas as pd
import numpy as np
import pymongo
import json
from sensor.config import Env_variable


# def test_execution():
#     try:
#         a=110
#         logging.info('Error check at main module {}'.format(a))
#         a/0
#     except Exception as e:
#         raise SensorException(e,sys)

# url ="mongodb+srv://vaibhavb108:******@cluster0.bpcbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# def dump_csvfile_to_mongodb(filepath:str,
#                             database_name:str,
#                             collection_name:str)->None: #since we dont want to return anythin we jsut want to pass
        
#         df= pd.read_csv(filepath)
#         df.reset_index(drop=True,inplace=True)
#         json_records=list(json.loads(df.T.to_json()).values())
#         mango_client= pymongo.MongoClient(url)
#         mango_client[database_name][collection_name].insert_many(json_records)
#         logging.info("Database loaded succesfully")
            


if __name__ == '__main__':  #it will run progm on only this page other import will restrict
    
    try:
        file_path= r'D:\Vaibhav_PC\Python\Project\SensorFault\aps_failure_training_set.csv'
        
        dump_csvfile_to_mongodb(file_path,'Sensor_DB','APS_sensor')
        
        # env= Env_variable()
        # print(env)

        
        
    except SensorException as e:
        print(e)
    



