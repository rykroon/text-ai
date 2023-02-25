from dataclasses import dataclass, asdict

from db import db
from .base import Document


collection = db['users']


@dataclass(kw_only=True)
class User(Document):
    first_name: str
    last_name: str
    phone_number: str


async def insert_one(first_name: str, last_name: str, phone_number: str):
    user = User(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )
    await collection.insert_one(asdict(user))
    return user


async def find_one(**kwargs):
    document = await collection.find_one(kwargs)
    if document is None:
        return None
    return User.from_document(document)
