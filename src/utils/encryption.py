import os
from cryptography.fernet import Fernet


FERNET_KEY = os.environ['FERNET_KEY']

f = Fernet(FERNET_KEY)
