import requests

import json

from base64 import b64decode

import os
from dotenv import load_dotenv

load_dotenv()

class TTSClient:

    def __init__(self):
        pass

    def get_audio(self, username):

        data = {
            "input": username,
            "voice_id": "lisa"
        }
        header = {
            "User-Agent":"HarkBot (https://github.com/marky0470, 0.1)",
            "Authorization": f"{os.getenv("TTS_API_KEY")}"
        }
        
        r = requests.post(url="https://api.speechify.ai/v1/audio/speech", data=json.dumps(data), headers=header)

        audio_data = b64decode(r.json()["audio_data"])

        return audio_data

