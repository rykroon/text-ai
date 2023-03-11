from dataclasses import dataclass
from typing import ClassVar, Literal
import uuid

from utils.db import db
from utils.crypt import encrypt_string, decrypt_bytes
from .documents import AuditDocument


@dataclass(kw_only=True)
class OpenAiChatMessage(AuditDocument):
    _collection: ClassVar = db["openai.chat.messages"]

    role: Literal["system", "user", "assistant"]
    encrypted_content: bytes
    user_uuid: uuid.UUID

    @classmethod
    def new(cls, *, content, **kwargs):
        encrypted_content = encrypt_string(content)
        return cls(encrypted_content=encrypted_content, **kwargs)

    @property
    def content(self) -> str:
        return decrypt_bytes(self.encrypted_content)

    @content.setter
    def content(self, content: str):
        self.encrypted_content = encrypt_string(content)
