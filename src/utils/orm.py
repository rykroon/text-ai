from dataclasses import asdict, dataclass, field, fields
import inspect
from typing import ClassVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor


class CursorWrapper:
    def __init__(self, class_, cursor):
        self.class_ = class_
        self.cursor = cursor

    def __aiter__(self):
        return self

    async def __anext__(self):
        document = await anext(self.cursor)
        return self.class_.from_document(document)


@dataclass
class Document:
    _collection: ClassVar[AsyncIOMotorCollection]
    _id: ObjectId = field(default_factory=ObjectId)

    @classmethod
    def new(cls, *args, **kwargs):
        sig = inspect.signature(cls)
        ba = sig.bind(*args, **kwargs)
        return cls(*ba.args, **ba.kwargs)

    @classmethod
    def from_document(cls, document: dict):
        field_names = (f.name for f in fields(cls))
        filtered_document = {f: document[f] for f in field_names if f in document}
        return cls(**filtered_document)

    @classmethod
    def find(
        cls,
        query: dict | None = None,
        skip: int = 0,
        limit: int = 0,
        sort: list[tuple[str, int]] | None = None,
    ) -> AsyncIOMotorCursor:
        cursor = cls._collection.find(filter=query, skip=skip, limit=limit, sort=sort)
        return CursorWrapper(cls, cursor)

    @classmethod
    async def find_one(cls, **kwargs):
        document = await cls._collection.find_one(kwargs)
        if document is None:
            return None
        return cls.from_document(document)

    async def insert(self):
        return await self._collection.insert_one(asdict(self))

    async def update(self):
        return await self._collection.update_one(
            filter={"_id": self._id}, update={"$set": asdict(self)}
        )

    async def delete(self):
        return await self._collection.delete_one({"_id": self._id})
