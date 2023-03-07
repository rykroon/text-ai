from dataclasses import dataclass
from typing import ClassVar, Literal
import uuid

from db import db
from .documents import Document


@dataclass(kw_only=True)
class OpenAiChatMessage(Document):
    _collection: ClassVar = db['openai.chat.messages']

    role: Literal['system', 'user', 'assistant']
    content: str
    user_uuid: uuid.UUID

