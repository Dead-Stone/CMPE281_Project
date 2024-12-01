from pymongo import MongoClient

mongo_client = None
mongo_db = None

def init_mongo_db():
    global mongo_client, mongo_db
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["project"]
