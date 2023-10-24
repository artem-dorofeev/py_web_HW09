from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import *

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
mongo_uri = config.get('DB', 'mongo_uri')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{mongo_uri}"



db = connect(host=uri, ssl=True, db="web8")


client = MongoClient(uri, server_api=ServerApi('1'))

