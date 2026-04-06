import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient():

    def __init__(self):
        self.client = MongoClient(f"{os.getenv("CONN_URI")}")
        self.collection = self.client.get_database('tts_audio').get_collection('audio')

    def get_audio(self, user_id) -> bytes | None:
        result = self.collection.find_one({"user_id": user_id})
        return result["audio_data"] if result else None

    def insert_audio(self, user_id: int, username: str, audio_data: bytes) -> None:
        data = {
            "user_id": user_id,
            "username": username,
            "use_audio": True,
            "audio_data": audio_data
        }
        self.collection.insert_one(data)

    def update_audio(self, user_id, audio_data: bytes) -> None:
        self.collection.update_one({"user_id": user_id}, {"$set": {"use_audio": True, "audio_data": audio_data}}, upsert=True)

    def get_use_audio(self, user_id) -> bool | None:
        result = self.collection.find_one({"user_id": user_id})
        return result["use_audio"] if result else None

    def update_use_audio(self, user_id, use_audio: bool) -> None:
        self.collection.update_one({"user_id": user_id}, {"$set": {"use_audio": use_audio}})

