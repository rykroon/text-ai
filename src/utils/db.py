import os
from motor.motor_asyncio import AsyncIOMotorClient


USERNAME = os.environ["MONGODB_USERNAME"]
PASSWORD = os.environ["MONGODB_PASSWORD"]
DBNAME = os.getenv("MONGODB_DBNAME", USERNAME)
HOST = os.environ["MONGODB_HOST"]

client = AsyncIOMotorClient(
    host=f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}", uuidRepresentation="standard"
)

db = client[DBNAME]
