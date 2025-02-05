#here we write how to share url/data to mongodb
from sensor.logger import logging
import pandas as pd
import numbers as np
import json
from sensor.config import mongo_client


def dump_csvfile_to_mongodb(filepath:str,
                            database_name:str,
                            collection_name:str)->None: #since we dont want to return anythin we jsut want to pass
    
    try:
        
        df= pd.read_csv(filepath)
        df.reset_index(drop=True,inplace=True)
        json_records=list(json.loads(df.T.to_json()).values())
        mongo_client[database_name][collection_name].insert_many(json_records)
        logging.info("Database loaded succesfully")
        
    except Exception as e:
        print(e)
        
        
        