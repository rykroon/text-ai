import os
import httpx

from .exceptions import TelnyxApiException


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]


client = httpx.AsyncClient(
    base_url="https://api.telnyx.com/",
    headers={"Authorization": f"Bearer {TELNYX_API_KEY}"},
    http2=True,
)


async def send_message(
    from_: str,
    to: str,
    text: str,
    media_urls: list[str] | None = None,
    webhook_url: str | None = None,
):
    data = {"from": from_, "to": to, "text": text, "webhook_url": webhook_url}

    if media_urls is not None:
        data["media_urls"] = media_urls

    resp = await client.post(url="/v2/messages", json=data)

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise TelnyxApiException.from_resp(resp)

    return resp.json()
