from base64 import b64decode
import os
import time
from typing import AnyStr

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey as PublicKey
import httpx


TELNYX_API_KEY = os.environ['TELNYX_API_KEY']
TELNYX_PUBLIC_KEY = os.environ['TELNYX_PUBLIC_KEY']


client = httpx.AsyncClient(
    base_url='https://api.telnyx.com/',
    headers={'Authorization': f"Bearer {TELNYX_API_KEY}"},
    http2=True
)


async def send_sms(from_: str, to: str, text: str, media_urls: list[str] | None = None):
    data = {
        'from': from_,
        'to': to,
        'text': text
    }

    if media_urls is not None:
        data['media_urls'] = media_urls

    resp = await client.post(
        url="/v2/messages",
        json=data
    )

    resp.raise_for_status()
    return resp.json()


def verify_webhook(
    payload: AnyStr,
    timestamp: AnyStr,
    signature: AnyStr,
    tolerance: int | None = None
) -> bool:
    if isinstance(payload, str):
        payload = payload.encode()
    
    if isinstance(timestamp, str):
        timestamp = timestamp.encode()
    
    if isinstance(signature, str):
        signature = signature.encode()

    message = timestamp + b"|" + payload
    public_key = PublicKey.from_public_bytes(b64decode(TELNYX_PUBLIC_KEY))

    try:
        public_key.verify(b64decode(signature), message)

    except InvalidSignature:
        return False
    
    if tolerance and int(timestamp) < time.time() - tolerance:
        return False
    
    return True
