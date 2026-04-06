from functools import lru_cache

from db_client import DatabaseClient
from tts_client import TTSClient

class AudioService:

    def __init__(self):
        self.db_client = DatabaseClient()
        self.tts_client = TTSClient()
        pass

    def get_audio(self, username: str, user_id: int) -> bytes:
        audio_data = self.db_client.get_audio(user_id)
        if audio_data is None:
            audio_data = self.tts_client.get_audio(username)
            self.db_client.insert_audio(user_id, username, audio_data)
        return audio_data

    # If we use these ever, need to make another method for inserting audio
    # def get_audio_from_db(self, user_id: int) -> bytes:
    #     return self.db_client.get_audio(user_id)

    # def get_audio_from_tts(self, username: str) -> bytes:
    #     return self.tts_client.get_audio(username)
    
    def update_audio(self, user_id: int, audio_data: bytes) -> None:
        self.db_client.update_audio(user_id, audio_data)
    
    def get_use_audio(self, user_id: int) -> bool | None: #ok to return None?
        return self.db_client.get_use_audio(user_id)    

    def update_use_audio(self, user_id: int, use_audio: bool) -> None:
        self.db_client.update_use_audio(user_id, use_audio)