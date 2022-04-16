import discord
from discord.ext import commands
from src.helpers.checks import check_guild


class Dev(commands.Cog):
	description = 'Komendy dla deweloperów bota' # Required field
	qualified_name = "Developer"

	
	def __init__(self, client):
		self.client = client

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # #                     H E L P E R S                   # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	@staticmethod
	def console(msg, who='cog'):
		print(f'[{__class__.__name__}] {who}\t\t: {msg}')
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # #                      E V E N T S                    # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	@commands.Cog.listener()
	async def on_ready(self):
		self.console('is ready')

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # #                    C O M M A N D S                  # # # # # # # # # # # # # # # #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	@commands.command(brief="Sprawdza ping bota")
	async def ping(self, ctx):
		print('dupa')
		await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")


def setup(client):
	client.add_cog(Dev(client))
