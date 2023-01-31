from base64 import b64decode
import os

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


TELNYX_PUBLIC_KEY = os.environ['TELNYX_PUBLIC_KEY']


def verify_signature(
    signature: bytes,
    timestamp: bytes,
    content: bytes
) -> bool:
    public_key = Ed25519PublicKey.from_public_bytes(
        b64decode(TELNYX_PUBLIC_KEY)
    )

    message = timestamp + b"|" + content
    try:
        public_key.verify(b64decode(signature), message)

    except InvalidSignature:
        return False
    
    return True
