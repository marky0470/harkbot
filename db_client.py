from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

"""
Infrequent writes, semifrequent reads
Maintain an open connection to DB, 
"""

class DatabaseClient():

    def __init__(self):
        self.client = MongoClient(f"{os.getenv("CONN_URI")}")
        self.collection = self.client.get_database('tts_audio').get_collection('audio')

    def get_audio(self, username):
        audio_data = self.collection.find_one({"name": username})
        return audio_data["audio_data"] if audio_data else None

    def insert_audio(self, username, audio_data):
        self.collection.insert_one({"name": username, "audio_data": audio_data})

    def update_audio(self, username, audio_data):
        self.collection.update_one({"name": username}, {"$set": {"audio_data": audio_data}})
