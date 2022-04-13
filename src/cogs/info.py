import discord
from discord.ext import commands
from res.links import urls

import platform


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Helpers
    @staticmethod
    def console(msg, who='cog'):
        print(f'[INFO] ({who})\t: {msg}')

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        self.console('is ready')

    # Commands
    @commands.command(brief="Zwraza podstawowe informacje o bocie", aliases=["informacje", "information", "aboutme"])
    async def info(self, ctx):
        await ctx.message.delete()  # Delete user message

        message = discord.Embed(
            title=f'Informacje o bocie {self.client.user.name}',
            color=discord.Color.random(),
        )

        message.set_thumbnail(url=self.client.user.avatar_url)

        field = ''
        for u in urls:
            field += f'• [{u}]({urls[u]})\n'

        message.add_field(name='GitHub', value=field)

        message.add_field(name='Informacje o serwerze',
                          value=f'{platform.system()}\n{platform.release()}{platform.architecture()[0]}\nPython {platform.python_version()}\ndiscord.py {discord.__version__}',
                          inline=False)

        message.set_footer(text=f'utworzono na prośbę {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=message)


def setup(client):
    client.add_cog(Info(client))
