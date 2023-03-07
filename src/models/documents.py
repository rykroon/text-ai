from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import ClassVar
from uuid import UUID, uuid4


from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor


@dataclass
class Document:
    _collection: ClassVar[AsyncIOMotorCollection]

    _id: ObjectId = field(default_factory=ObjectId)
    uuid: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_document(cls, document: dict):
        return cls(**document)

    @classmethod
    def find(
        cls,
        query: dict | None = None,
        projection: dict | None = None,
        skip: int = 0,
        limit: int = 0,
        sort: list[tuple[str, int]] | None = None
    ) -> AsyncIOMotorCursor:
        return cls._collection.find(
            filter=query,
            projection=projection,
            skip=skip,
            limit=limit,
            sort=sort
        )

    @classmethod
    async def find_one(cls, **kwargs):
        document = await cls._collection.find_one(kwargs)
        if document is None:
            return None
        return cls.from_document(document)

    async def insert(self):
        result = await self._collection.insert_one(asdict(self))
    
    async def update(self):
        self.updated_at = datetime.utcnow()
        result = await self._collection.update_one(asdict(self))

    async def delete(self):
        result = await self._collection.delete_one({'_id': self._id})
