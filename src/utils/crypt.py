import os
from cryptography.fernet import Fernet


FERNET_KEY = os.environ["FERNET_KEY"]

f = Fernet(FERNET_KEY)


def encrypt_string(s: str) -> bytes:
    return f.encrypt(s.encode())


def decrypt_bytes(b: bytes) -> str:
    f.decrypt(b).decode()
