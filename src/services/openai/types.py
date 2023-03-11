from typing import Literal, TypedDict


class Message(TypedDict):
    """
    https://platform.openai.com/docs/guides/chat/introduction
    """

    role: Literal["assistant", "system", "user"]
    content: str
