from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from bson import ObjectId


@dataclass
class Document:
    _id: ObjectId = field(default_factory=ObjectId)
    uuid: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_document(cls, document: dict):
        return cls(**document)
