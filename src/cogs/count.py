import discord
from discord.ext import commands


class Counter(commands.Cog):
	counting_channel_ID = 0
	
	def __init__(self, client):
		self.client = client

	def getID(self):
		return self.counting_channel_ID

	# Helpers
	@staticmethod
	def console(msg):
		print(f'[COUNTER] (cog)\t: {msg}')

		
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		self.console('is ready')

	# Commands
	@commands.command(brief="Krótki opis", aliases=["licz", "count"])
	async def liczenie(self, ctx, *, stringToParse=None):		
		if self.counting_channel_ID != 0:
			await ctx.send(f'Już utworzono kanał do liczenia: <#{self.counting_channel_ID}>')
			return
		
		if stringToParse is None:
			await ctx.send(f'Sprobuj `{str(ctx.message.content)} \'nazwa kanału do liczenia\'`')
			self.console('None')
		else:
			# Find channel_id by name
			for channel in ctx.guild.channels:
				if channel.name == stringToParse:
					self.counting_channel_ID = channel.id
					self.console(f'Creating counting channel on #{stringToParse}')
					await ctx.send(f'Kanał <#{self.counting_channel_ID}> został ustawiony jako kanał do liczenia!')
					return

			await ctx.send(f'Nie znaleziono kanału o nazwie #{stringToParse} ID: {self.counting_channel_ID}')

def setup(client):
	client.add_cog(Counter(client))
