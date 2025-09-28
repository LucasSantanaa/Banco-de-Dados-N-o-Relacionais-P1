from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime, timezone
from bson.objectid import ObjectId


class MessageIn(BaseModel):
    username: constr(strip_whitespace=True, min_length=1, max_length=50)
    content: constr(strip_whitespace=True, min_length=1, max_length=1000)

class MessageOut(BaseModel):
    id: str = Field(..., alias="_id")
    room: str
    username: str
    content: str
    created_at: str

    class Config:
        allow_population_by_field_name = True

def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

def serialize(doc: dict) -> dict:
    d = dict(doc)
    if '_id' in d and isinstance(d['_id'], ObjectId):
        d['_id'] = str(d['_id'])
    if 'created_at' in d and isinstance(d['created_at'], datetime):
        d['created_at'] = _iso(d['created_at'])
    return d
