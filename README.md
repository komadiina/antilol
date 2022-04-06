# antilol.py
  
saw a similar snippet online that bans league players from the server, however it's too much so i decided to publicly shame every league player
  
the code itself is pretty self-explanatory, however there are some things you should raise attention to, especially in the dotenv (`.env`) variables file, located in the root directory.

- `DISCORD_TOKEN` : your discord OAuth2 token, found in your discord's devsite (in .env : `DISCORD_TOKEN`)
- `DISCORD_GUILD` : the name of your discord server (*case-sensitive*) (in .env : `DISCORD_GUILD`)
- `DISCORD_SERVER_ID` : used for updating guild data whenever the bot is ran, found in **Server Settings - Widgets** (in .env : `DISCORD_SERVER_ID`)
- `TARGET_CHANNEL` : the channel ID where the spam should go to, *developer mode* must be enabled in discord discord app settings. (in .env : `DISCORD_MAIN_CHANNEL_ID`)

___

*Main code:*

```py
# ... in class MyClient(discord.Client) ...
client = discord.Client()

async def on_ready(self):
    # ...
    client.check_for_nolifers.start() # loop's start signal
    # ...

# ...

@tasks.loop(seconds=5, counts=None, reconnect=True)
    async def check_for_nolifers(self):
        print(f'LOG: checking for targets...')
        for member in self.get_all_members():
            for activity in member.activities:
                print(f'\t> {member.name} is playing {activity.name}')

                if activity.name == 'League of Legends':
                    channel = client.get_channel(CHANNEL)
                    await channel.send(f'<@{member.id}> is playing {activity.name} lol @everyone')
```

*notes:*  

- `@tasks.loop(seconds=(int), counts=(int) / 'None', reconnect=(bool))`  
  - `seconds=(int)` == `minutes=(int)` == `hours=(int)` : specified time interval of how often the loop should be ran.  
  - `counts= (int) or None` : signal how many times the loop should be ran (`None` if infinitely)
  - `reconnect = (bool)` : determines should the coroutine restart if an (unexpected) error occurs
- `channel = client.get_channel(CHANNEL)` : specifies the target channel to spam into via its ID  
- alternatively, for the app to work independently of user's locale, `activity.name` could be replaced with `activity.application_id`, see [here](https://discordpy.readthedocs.io/en/stable/api.html#activity).  
- `await channel.send(message)` : message that should be sent whenever the specified activity is detected.
