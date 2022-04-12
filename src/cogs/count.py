import discord
from discord.ext import commands
import asyncio

# TODO Przyponanie co `x` wiadomosci, badz inna akcja nagrody
# `x` może byc wielokrotnoscia 10 wybierana losowo

class Counter(commands.Cog):
	counting_channel_ID = int(0)
	last_user_ID = 0
	next_number = 1
	
	def __init__(self, client):
		self.client = client

	# Helpers
	@staticmethod
	def console(msg, who='cog'):
		print(f'[COUNTER] ({who})\t: {msg}')

	@staticmethod
	def reset(self):
		self.counting_channel_ID = int(0)
		self.last_user_ID = 0
		self.next_number = 1
		
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		self.console('is ready')
	
	@commands.Cog.listener()
	async def on_message(self, message = discord.message):
		if message.author.bot:
			return
		if message.channel.id == self.counting_channel_ID:
			if message.content != str(self.next_number) or self.last_user_ID == message.author.id:
				await message.delete()
				return
			self.next_number += 1
			self.last_user_ID = message.author.id
			await message.add_reaction('👍')
				
	# Commands
	@commands.command(brief="Krótki opis", aliases=["licz", "count"])
	async def liczenie(self, ctx, *, stringToParse=None):		
		if self.counting_channel_ID != 0:
			await ctx.send(f'Już utworzono kanał do liczenia: <#{self.counting_channel_ID}>')
			return
		
		if stringToParse is None:
			await ctx.send(f'Sprobuj `{str(ctx.message.content)} \'nazwa kanału do liczenia\'`')
		else:
			# Find channel_id by name
			for channel in ctx.guild.channels:
				if channel.name == stringToParse:
					self.counting_channel_ID = channel.id
					self.console(f'created counting channel on #{stringToParse}', ctx.author.display_name)
					await ctx.send(f'Kanał <#{channel.id}> został ustawiony jako kanał do liczenia!')
					await channel.edit(topic='To infinity and beyond!')
					return

			await ctx.send(f'Nie znaleziono kanału o nazwie #{stringToParse}')
			self.console(f'tried to create counting channel {stringToParse}', ctx.author.display_name)
			

	@commands.command(brief="Odpina kanał do liczenia")
	async def odepnij(self, ctx, *, stringToParse=None):
		if stringToParse == 'reset':
			self.reset()
			await ctx.send('Przywrócono wartości początkowe dla modułu')
			return
		
		if self.counting_channel_ID == 0:
			await ctx.send(f'Nie utworzono kanału do liczenia')
			return
		elif stringToParse is None:
			await ctx.send(f'Aby odpiąć kanał <#{self.counting_channel_ID}> wpisz: `{str(ctx.message.content)} \'nazwa kanału do liczenia\'`')
			return
	
		channel = discord.utils.get(ctx.guild.channels, name=stringToParse)
		if channel.id == self.counting_channel_ID:
			self.reset(self)
			self.console(f'removed counting channel on #{stringToParse}', ctx.author.display_name)
			await ctx.send(f'Odpięto kanał <#{channel.id}>')
			await channel.edit(topic=None)
			return
		await ctx.send('Niepoprawna nazwa kanału')
		
# Setup	
def setup(client):
	client.add_cog(Counter(client))
