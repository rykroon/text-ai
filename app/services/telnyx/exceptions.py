from dataclasses import dataclass
from httpx import Response


class TelnyxException(Exception):
    ...


class InvalidTelnyxSignature(TelnyxException):
    ...


@dataclass
class TelnyxApiException(TelnyxException):
    code: str
    title: str
    detail: str

    def __post_init__(self):
        super().__init__(self.code, self.title, self.detail)

    @classmethod
    def from_resp(cls, resp: Response):
        result = resp.json()
        error = result['errors'][0]
        return cls(
            code=error['code'],
            title=error['title'],
            detail=error['detail']
        )
