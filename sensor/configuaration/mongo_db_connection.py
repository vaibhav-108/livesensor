import os
import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import certifi
from sensor.logger import logging

ca= certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongoDBClient.client is None:
            mongo_db_url = os.getenv(MONGODB_URL_KEY)
            logging.info(f"MongoDB url recewived:-  {mongo_db_url}")
            
            if mongo_db_url is None:
                raise Exception(f"Environment variable: {MONGODB_URL_KEY} is not set.")
            if 'localhost' in mongo_db_url:
                logging.info(f"Connecting to MongoDB in local mode.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            else:
                logging.info(f"Connecting to MongoDB in cloud mode.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
        self.client = MongoDBClient.client
        self.database = self.client[database_name]
        self.database_name = database_name
