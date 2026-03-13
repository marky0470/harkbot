from pymongo import MongoClient

from db_client import DatabaseClient
from tts_client import TTSClient

import os
from dotenv import load_dotenv

from functools import lru_cache

load_dotenv()

class AudioService:

    def __init__(self):
        self.db_client = DatabaseClient()
        self.tts_client = TTSClient()
        pass

    def get_audio(self, username):
        return self.get_audio_from_db(username) or self.get_audio_from_tts(username)

    def get_audio_from_db(self, username):
        return self.db_client.get_audio(username)

    def get_audio_from_tts(self, username):
        audio_data = self.tts_client.get_audio(username)
        self.db_client.insert_audio(username, audio_data)
        return audio_data
    
    def update_audio(self, username, audio_data):
        self.db_client.update_audio(username, audio_data)