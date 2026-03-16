from discord import Attachment

help_message = """\t
    !!setself -Sets the user's audio file to attachment given
    !!setuser <user_id> -Sets specified user's audio file to attachment given, using ID
        - setself and setuser will always do !!hark in the background when run
    !!setchannel <channel_id> -Sets the target channel
    !!hark -Sound will be played for the sender of this command
    !!nohark -No sound will be played for the sender of this command
    !!play <user_id> -Play the sound of the user id provided
"""

class CommandHandler:

    def __init__(self, bot):
        self.bot = bot
        pass

    #TODO: !!setaudio, if no additional param, set author's audio, otherwise use id passed in, same for !!hark and !!nohark (priviledged roles can disable other user harks, )
    async def handle_command(self, command):
        cmd, *args = command.content.split(" ")
        author = command.author
        self.last_command_channel = command.channel
        match cmd:
            case "!!help":
                await command.channel.send(help_message)
            case "!!setself":
                await self.update_audio_for_user(author.id, command.attachments[0])
            case "!!setuser":
                await self.update_audio_for_user(int(args[0]), command.attachments[0])
            case "!!setchannel":
                await self.update_target_channel(int(args[0]))
            case "!!hark":
                await self.update_use_audio_for_user(author.id, True)
            case "!!nohark":
                await self.update_use_audio_for_user(author.id, False)
            case "!!play":
                await self.bot.play_audio(int(args[0])) #add message
            case _:
                await command.channel.send("Unknown command, use !!help to view available commands")

    async def update_target_channel(self, target_channel_id: int):
        bot = self.bot
        target_channel = bot.get_channel(target_channel_id)
        if target_channel is None:
            await self.last_command_channel.send("No channel with that ID found.")
            return
        await self.last_command_channel.send(f"Setting target channel to channel {target_channel}.")
        bot.set_target_channel(target_channel)
        if bot.voice_clients: await bot.voice_clients[0].disconnect()
        
    async def update_audio_for_user(self, user_id: int, attachment: Attachment):
        bot = self.bot
        user = bot.guilds[0].get_member(user_id)
        if user is None:
            await self.last_command_channel.send("No user with that ID found.")
            return
        await self.last_command_channel.send(f"Setting audio for user: {user.name}, enabling HarkBot for them.") 
        audio_data = await attachment.to_file()
        bot.audio_service.update_audio(user_id, audio_data.fp.read())

    async def update_use_audio_for_user(self, user_id: int, use_audio: bool):
        await self.last_command_channel.send(f"{"Enabled" if use_audio else "Disabled"} HarkBot for you.")
        self.bot.audio_service.update_use_audio(user_id, use_audio) 

#questions: how much responsibility should command handler's hold? should the functions immediately delegate to the appropriate class
# and leave validation and status messages to them?