import asyncio
from os import getenv

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient

load_dotenv()

def get_db_client():
    client: MongoClient = AsyncIOMotorClient(getenv("DB_SRV"))

    # Attaches the client to the same loop
    client.get_io_loop = asyncio.get_event_loop
    print("USING REAL DB")
    return client


