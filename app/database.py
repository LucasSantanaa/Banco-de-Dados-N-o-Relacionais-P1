"""Conexão com MongoDB."""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URL, MONGO_DB

_client: Optional[AsyncIOMotorClient] = None

def get_db():
    global _client
    if _client is None:
        if not MONGO_URL:
            raise RuntimeError("Defina MONGO_URL no .env")
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client[MONGO_DB]
