from base64 import b64decode
import os
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .exceptions import InvalidTelnyxSignature


TELNYX_PUBLIC_KEY = os.environ["TELNYX_PUBLIC_KEY"]


def verify_signature(
    signature: bytes, timestamp: bytes, content: bytes, tolerance: int = 0
) -> bool:
    public_key = Ed25519PublicKey.from_public_bytes(b64decode(TELNYX_PUBLIC_KEY))

    message = timestamp + b"|" + content
    try:
        public_key.verify(b64decode(signature), message)

    except InvalidSignature:
        raise InvalidTelnyxSignature from InvalidSignature

    if int(timestamp) < time.time() - tolerance:
        raise InvalidTelnyxSignature
