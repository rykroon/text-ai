from dataclasses import dataclass
from httpx import Response


@dataclass
class OpenAiException(Exception):
    message: str
    type: str
    param: str | None
    code: str | None

    def __post_init__(self):
        super().__init__(self, self.message, self.type, self.param, self.code)

    @classmethod
    def from_resp(cls, resp: Response):
        result = resp.json()
        error = result["error"]
        return cls(
            message=error["message"],
            type=error["type"],
            param=error["param"],
            code=error["code"],
        )
