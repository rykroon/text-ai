from dataclasses import dataclass
from typing import ClassVar

from utils.db import db
from .documents import AuditDocument


@dataclass(kw_only=True)
class AccessNumber(AuditDocument):
    _collection: ClassVar = db["numbers"]

    phone_number: str
    service: str
