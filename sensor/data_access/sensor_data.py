import sys
from typing import Optional
import numpy as np
import pandas as pd
import json

from sensor.configuaration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME,COLLECTION_NAME
from sensor.exception import SensorException

class SensorData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            print(self.mongo_client)
            self.database_name = DATABASE_NAME
            self.database = self.mongo_client.database
        except Exception as e:
            raise SensorException(e, sys)
        
    def save_csv_file(self,filepath,collection_name:str,database_name:Optional[str]=None):
        try:
            dataframe = pd.read_csv(filepath)
            dataframe.reset_index(drop=True, inplace=True)
            records = list(json.loads(dataframe.T.to_json()).values())
            if database_name is None:
                collection = self.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            collection.insert_many(records)
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def export_collection_as_df(self, collection_name:str, database_name:Optional[str]=None) -> pd.DataFrame:
        """It weill export all the collections in the form of pd.dataframe
        """
        
        try:
            if database_name is None:
                collection = self.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
                
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise SensorException(e, sys)
        