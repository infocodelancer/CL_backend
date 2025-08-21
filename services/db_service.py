from typing import Dict
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timezone
from config import settings

_client = None
_db = None
_customers = None

def _get_client() -> MongoClient:
    global _client, _db, _customers
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
        _db = _client[settings.DB_NAME]
        _customers = _db["customers"]
        # Ensure useful indexes
        _customers.create_index("email", unique=False)
        _customers.create_index([("createdAt", 1)])
    return _client

def customers_collection():
    _get_client()
    return _customers

def insert_customer(doc: Dict) -> str:
    """
    Insert a customer document, with server-set timestamps.
    """
    try:
        col = customers_collection()
        doc["createdAt"] = datetime.now(timezone.utc)
        doc["updatedAt"] = doc["createdAt"]
        result = col.insert_one(doc)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise RuntimeError(f"MongoDB error: {e}")
