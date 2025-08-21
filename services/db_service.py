from typing import Dict, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timezone
from config import settings

_client = None
_db = None
_customers = None
_super_admins = None


def _get_client() -> MongoClient:
    global _client, _db, _customers, _super_admins
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
        _db = _client[settings.DB_NAME]

        # Customers collection
        _customers = _db["customers"]
        _customers.create_index("email", unique=False)
        _customers.create_index([("createdAt", 1)])

        # Super admins collection
        _super_admins = _db["super_admin"]

    return _client


def customers_collection():
    _get_client()
    return _customers


def super_admin_collection():
    _get_client()
    return _super_admins


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


def get_super_admin_emails() -> List[str]:
    """
    Fetch all super admin emails from the `super_admin` collection.
    Each document should contain at least: {"email": "admin@example.com"}.
    """
    try:
        col = super_admin_collection()
        admins = col.find({}, {"email": 1, "_id": 0})
        return [a["email"] for a in admins if "email" in a]
    except PyMongoError as e:
        raise RuntimeError(f"MongoDB error: {e}")
