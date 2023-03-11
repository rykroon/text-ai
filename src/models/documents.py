from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from utils.orm import Document


@dataclass(kw_only=True)
class AuditDocument(Document):

    uuid: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    async def update(self):
        self.updated_at = datetime.utcnow()
        return super().update()
