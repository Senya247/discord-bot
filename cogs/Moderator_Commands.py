from discord.ext import commands


class ModeratorCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Clear the last x messages", hidden=True)
    @commands.is_owner()
    async def clear(self, ctx, amount=0):
        if ctx.author.id == 778169357481279518:
            return
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(ModeratorCommands(client))
