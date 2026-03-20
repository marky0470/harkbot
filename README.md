# HarkBot
Discord Bot that announces who has connected to the voice channel. Users can also upload custom audio following the various commands available. Uses pymongo for interacting with a MongoDB Atlas database, and gets TTS audio data from Speechify's API

### Commands
    !!help -Displays a list of commands
    !!setself -Sets the user's audio file to attachment given
    !!setuser <user_id> -Sets specified user's audio file to attachment given, using ID
        - setself and setuser will always do !!hark in the background when run
    !!setchannel <channel_id> -Sets the target channel
    !!hark -Sound will be played for the sender of this command
    !!nohark -No sound will be played for the sender of this command
    !!play <user_id> -Play the sound of the user id provided

### TODO
- proper file structure
- combine !!setself and !!setuser
- validate audio attachment (max duration)
