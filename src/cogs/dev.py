import discord
from discord.ext import commands
from src.helpers.checks import check_guild


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                     H E L P E R S                   # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                      E V E N T S                    # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} is ready.')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                    C O M M A N D S                  # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @commands.command(brief="Sprawdza ping bota")
    async def ping(self, ctx):
        print('dupa')
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")


def setup(client):
    client.add_cog(Dev(client))
