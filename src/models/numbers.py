from dataclasses import dataclass
from typing import ClassVar

from db import db
from .documents import Document


@dataclass(kw_only=True)
class AccessNumber(Document):
    _collection: ClassVar = db['numbers']

    phone_number: str
    service: str
