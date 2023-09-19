from discord.ext import tasks, commands
import discord
import os


class Loops(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.x = 23

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Game(next(self.statuses)))

    @tasks.loop(seconds=600)
    async def res(self):
        os.system('python3 /home/runner/discord-bot/cogs/Schedule_Downloader.py')

def setup(client):
    client.add_cog(Loops(client))
