from pymongo import MongoClient
import datetime

class MongoHandler:
    def __init__(self, db_name="riscv_translator", collection_name="translations"):
        self.client = MongoClient("mongodb+srv://aaf9407:@cluster0.pmxxs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def store_translation(self, binary_code, assembly_code):
        """ Store a translated instruction in MongoDB """
        record = {
            "binary_code": binary_code,
            "assembly_code": assembly_code,
            "timestamp": datetime.datetime.utcnow()
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