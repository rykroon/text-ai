from dataclasses import dataclass, asdict

from db import db
from .base import Document

collection = db['numbers']


@dataclass(kw_only=True)
class AccessNumber(Document):
    phone_number: str
    service: str


async def insert_one(phone_number: str, service: str):
    number = AccessNumber(
        phone_number=phone_number,
        service=service
    )
    await collection.insert_one(asdict(number))


async def find_one(**kwargs):
    document = await collection.find_one(kwargs)
    if document is None:
        return None
    return AccessNumber.from_document(document)
