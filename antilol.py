import asyncio
import discord
import os
from discord.ext import commands
from discord.ext import tasks
from distutils.command import check
from dotenv import load_dotenv
from idna import check_hyphen_ok


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SERVER_ID = os.getenv('DISCORD_SERVER_ID')
CHANNEL = os.getenv('TARGET_CHANNEL')

intents = discord.Intents.all()


class MyClient(discord.Client):
    client = discord.Client()

    # enable on/off states via message commands
    # here you can also use @bot.Command() variation
    @client.event
    async def on_message(self, msg):
        if msg.author != self.user:
            if msg.content.startswith('$stopshaming'):
                client.check_for_nolifers.stop()
                print(f'LOG: aborted shaming process')
                await msg.channel.send('*stopping shaming... ($startshaming to continue)*')
            elif msg.content.startswith('$startshaming'):
                client.check_for_nolifers.start()
                print(f'LOG: continued shaming process')
                await msg.channel.send('**continuing shaming ^__^...**')

    @client.event
    async def on_ready(self):
        print('LOG: logged in as {0.user}'.format(client))
        client.check_for_nolifers.start()

    async def update_guild(self):
        self.guild = await self.client.get_guild(SERVER_ID)

    # main code
    @tasks.loop(seconds=5, counts=None, reconnect=True)
    async def check_for_nolifers(self):
        print(f'LOG: checking for nolifers...')
        for member in self.get_all_members():
            for activity in member.activities:
                print(f'\t> {member.name} is playing {activity.name}')

                if activity.name == 'League of Legends':
                    channel = client.get_channel(CHANNEL)
                    await channel.send(f'<@{member.id}> is playing {activity.name} lol @everyone')


client = MyClient(intents=intents)

client.run(TOKEN)
