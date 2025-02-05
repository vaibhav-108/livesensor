# we are transfereing csv file to mongoDB atlass
from dotenv import load_dotenv
from dataclasses import dataclass
import os
import pymongo

load_dotenv()

@dataclass
class Env_variable():
    mongo_db_url:str= os.getenv('MONGO_DB_URL')  #it will call url from .env
    
    
    
env_var= Env_variable()

mongo_client= pymongo.MongoClient(env_var.mongo_db_url)

