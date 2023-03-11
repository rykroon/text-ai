from dataclasses import dataclass
from typing import ClassVar

from utils.db import db
from .documents import AuditDocument


@dataclass(kw_only=True)
class User(AuditDocument):
    _collection: ClassVar = db["users"]

    first_name: str
    last_name: str
    phone_number: str
