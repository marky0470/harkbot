import io

import discord

from audio_service import AudioService
from command_handler import CommandHandler
from config_helper import ConfigHelper

class Bot(discord.Client):

    def __init__(self, *, intents, **options):
        self.audio_service = AudioService()
        self.command_handler = CommandHandler(self)
        self.config_helper = ConfigHelper()
        super().__init__(intents=intents, **options)
    
    #TODO: cfg - only hark for users that have !!hark(ed) once opt-in: true -> users joining | no-tts: bool -> no tts audio
    async def on_ready(self):
        target_channel = self.config_helper.get_config("target_channel")
        self.target_channel = self.get_channel(target_channel)

    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            return
        
        target_channel = self.target_channel
        joined_target = (before.channel is not target_channel and after.channel is target_channel)
        left_target = not joined_target

        if joined_target:
            if len(target_channel.members) >= 1:
                await self.play_audio(member.id, member.name)
        elif left_target:
            if len(target_channel.members) <= 1 and self.voice_clients:
                await self.voice_clients[0].disconnect()
   
    async def on_message(self, message):
        if not message.content.startswith("!!") or message.author == self.user:
            return
        await self.command_handler.handle_command(message)

    async def play_audio(self, user_id: int, username: str = None): #make the chain not dependent on username, userid only
        if self.audio_service.get_use_audio(user_id) == False:
            return
        
        if not self.voice_clients:
            await self.target_channel.connect()
            
        audio_data = self.audio_service.get_audio(username, user_id)
        self.voice_clients[0].play(discord.FFmpegPCMAudio(pipe=True, source=io.BytesIO(audio_data)))

    def set_target_channel(self, target_channel: discord.Channel):
        self.config_helper.set_config("target_channel", target_channel.id)
        self.target_channel = target_channel
