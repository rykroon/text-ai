import os
import httpx


TELNYX_API_KEY = os.environ['TELNYX_API_KEY']


client = httpx.AsyncClient(
    base_url='https://api.telnyx.com/',
    headers={'Authorization': f"Bearer {TELNYX_API_KEY}"}
)


async def send_sms(from_: str, to: str, text: str):
    resp = await client.post(
        url="/v2/messages",
        json={
            'from': from_,
            'to': to,
            'text': text
        }
    )
    resp.raise_for_status()
    return resp.json()
