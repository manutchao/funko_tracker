import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ.get("DB_NAME", "funko")]
funkos_collection = db["funkos"]