import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read individual components from .env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Build the connection string
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """Establishes a connection to the MongoDB database."""
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        print("Database connection established.")

    def close(self):
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()
            print("Database connection closed.")

# Create a single instance of the MongoDB connection manager
mongodb_connection = MongoDB()

# A convenience function to get the database object
async def get_database():
    if mongodb_connection.db is None:
        mongodb_connection.connect()
    return mongodb_connection.db