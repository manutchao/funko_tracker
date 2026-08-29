import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME", "funko")

if not MONGO_URI:
    logging.warning(
        "MONGO_URI not set. Falling back to localhost MongoDB at mongodb://localhost:27017. "
        "Set MONGO_URI in .env for production."
    )
    MONGO_URI = "mongodb://localhost:27017"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command("ping")
except Exception as e:
    logging.error(f"Could not connect to MongoDB at {MONGO_URI}: {e}")
    raise RuntimeError(f"MongoDB connection failed: {e}")

db = client[DB_NAME]
funkos_collection = db["funkos"]
