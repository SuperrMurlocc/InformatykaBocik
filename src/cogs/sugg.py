from turtle import textinput
from types import TracebackType
import discord
from discord.ext import commands
from random import randint

class NewCog(commands.Cog):

	CHANNEL_NAME = 'bot-sugestie'
	ID_LENGTH = 4

	def __init__(self, client):
		self.client = client

	# Helpers
	@staticmethod
	def console(msg, who='cog'):
		print(f'[SUGG] ({who})\t: {msg}')

	@staticmethod
	def random_with_N_digits(n):
		range_start = 10**(n-1)
		range_end = (10**n)-1
		return randint(range_start, range_end)
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		# Create suggestions channel if missing

		self.console('is ready')
		
	# Commands
	@commands.command(brief="komenda testowa", aliases=["sugestia", "suggest"])
	async def sugg(self, ctx, *, stringToParse=None):
		if stringToParse is None:
			await ctx.send(f"Użyj: `{ctx.message.content} 'Sugestia do wysłania'`\n*Twoja sugestia zostanie wysłana do administratorów serwera*")
			return

		if not any(self.CHANNEL_NAME in channel.name for channel in ctx.guild.channels):
        	# Create suggestions channel
			ch = await ctx.guild.create_text_channel(self.CHANNEL_NAME)
			await ctx.channel.send('Utworzono kanał do wysyłania sugestii')
			self.console('Created {self.CHANNEL_NAME} suggestions channel', ctx.message.author.display_name)

		id = str(self.random_with_N_digits(self.ID_LENGTH))
		embd = discord.Embed(title=f"Sugestia # {id}", description=stringToParse, color=discord.Color.random())
		embd.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

		channel = discord.utils.get(ctx.guild.channels, name=self.CHANNEL_NAME)
		await channel.send(embed = embd)
		await ctx.channel.send(f'Dziękujemy za pomoc! `ID: #{id}`')
		self.console(f'suggestion #{id} received', ctx.message.author.display_name)



def setup(client):
	client.add_cog(NewCog(client))
