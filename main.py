from audio_service import AudioService

import discord

import io
from base64 import b64decode

import os
from dotenv import load_dotenv

load_dotenv()

class Bot(discord.Client):

    def __init__(self, *, intents, **options):
        self.audio_service = AudioService()
        super().__init__(intents=intents, **options)
        
    async def on_ready(self):
        self.target_channel = self.get_channel(1040523486864621628)
        pass

    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            return
    
        if before.channel is not self.target_channel and after.channel is self.target_channel:
            if len(self.target_channel.members) >= 1:
                await self.target_channel.connect()
                audio_data = self.audio_service.get_audio(member.name)
                self.voice_clients[0].play(discord.FFmpegPCMAudio(pipe=True, source=io.BytesIO(audio_data)))

        elif before.channel is self.target_channel and after.channel is not self.target_channel:
            if len(self.target_channel.members) <= 1 and self.voice_clients:
                await self.voice_clients[0].disconnect()
    """
    !!setself -Sets the user's audio file to attached embed
    !!setuser <user> -Sets specified user's audio file to attached embed
    !!nohark -No custom sound will be played for the sender of this command
    """
    async def on_message(self, message):
        if not message.content.startswith("!!"):
            return
    
        m = message.content.split(" ")
        match m[0]:
            case "!!setself":
                print("setself detected, updating audio...")
                audio_data = await message.attachments[0].to_file()
                self.audio_service.update_audio(message.author.name, audio_data.fp.read())
        # if message.channel == self.get_channel(1481607481820975104) and message.author != self.user:
        #     await message.channel.send("Message detected")
        #     print(message.attachments)
        # pass

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

b = Bot(command_prefix="", intents=intents)

b.run(os.getenv('DISCORD_KEY'))


