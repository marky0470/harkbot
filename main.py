import os

import discord
from dotenv import load_dotenv

from bot import Bot

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

b = Bot(intents=intents)

b.run(os.getenv('DISCORD_KEY'))
