from dataclasses import dataclass
from typing import ClassVar

from db import db
from .documents import Document


@dataclass(kw_only=True)
class User(Document):
    _collection: ClassVar = db['users']

    first_name: str
    last_name: str
    phone_number: str
