from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
load_dotenv()
class MongoHandler:
    def __init__(self, db_name="riscv_translator", collection_name="translations"):
        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise ValueError("Error: MONGODB_URI is not set. Please set it in an environment variable or .env file.")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def store_translation(self, binary_code, assembly_code):
        """ Store a translated instruction in MongoDB """
        record = {
            "binary_code": binary_code,
            "assembly_code": assembly_code,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        self.collection.insert_one(record)

    def get_translation(self, binary_code):
        """ Retrieve a translation if it exists """
        record = self.collection.find_one({"binary_code": binary_code})
        return record["assembly_code"] if record else None

    def get_translation_history(self, limit=10):
        """ Retrieve the last `limit` translations """
        history = self.collection.find().sort("timestamp", -1).limit(limit)
        return list(history)