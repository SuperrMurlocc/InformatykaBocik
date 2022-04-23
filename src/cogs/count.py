import discord
from discord.ext import commands
from res.plodz import author_img
from src.helpers.secrets import load_secrets, get_secret
import requests
import deepl
import random

load_secrets()
DEEPL_KEY = get_secret('DEEPL')
translator = deepl.Translator(DEEPL_KEY)

class Counter(commands.Cog):
	description = 'Obsługa kanału do liczenia' # Required field
	qualified_name = "Liczenie"
	
	counting_channel_ID = int(0)
	default_channel_name = 'liczenie'
	last_user_ID = 0
	next_number = 1
	responses = ['👌', '👍', '🥳', '😄', '😺', '🙆‍♀️', '🙆‍♂️', '🆗', '✅', '✨']
	
	def __init__(self, client):
		self.client = client

	# Helpers
	@staticmethod
	def console(msg, who='cog'):
		print(f'[{__class__.__name__}] {who}\t: {msg}')

	@staticmethod
	def reset(self):
		self.counting_channel_ID = int(0)
		self.last_user_ID = 0
		self.next_number = 1
		
	# Events
	@commands.Cog.listener()
	async def on_ready(self):

		# Check if the channel with default_channel_name already exists
		# Find channel_id by name
		for channel in self.client.guilds[0].channels:
			if channel.name == self.default_channel_name:
				self.counting_channel_ID = channel.id
				self.console(f'Found channel {self.default_channel_name}')
				
				# Load saved number
				pins = await channel.pins()
				for m in pins:
					self.next_number = int(m.content) + 1
					self.last_user_ID = m.author.id
				return
				
		self.console(f'Did not found channel {self.default_channel_name}')



	@commands.Cog.listener()
	async def on_message(self, message = discord.message):
		#Remove pinned messages from bot
		if message.type == "PINS_ADD" and message.author.bot:
			message.delete()
		if message.author.bot:
			return
		if message.channel.id == self.counting_channel_ID:
			if message.content != str(self.next_number) or self.last_user_ID == message.author.id:
				await message.delete()
				return
			self.next_number += 1
			self.last_user_ID = message.author.id
			emoji = random.choice(self.responses)

			await message.add_reaction(emoji)
			# Clear pinned messages (autosave)
			pins = await message.channel.pins()
			for m in pins:
				if m is not None:
					await m.unpin()

			# Autosave
			await message.pin()

			# Get a fact of the number from Numbers API
			url = f'http://numbersapi.com/{message.content}/?default=0'
			api_response = requests.get(url)

			if not api_response.ok:
				self.console(f'Failed request call on number {message.content}','numbers API')
				return
			if api_response.text != '0':
				
				translated = translator.translate_text(api_response.text, target_lang="PL")
				info_tuple = random.choice(author_img)
				em = discord.Embed(
					description=translated,
					color = info_tuple[0],
				)
				em.set_author(name=info_tuple[1], icon_url=info_tuple[2])
				await message.channel.send(embed=em)

				
	# Commands
	@commands.command(brief="Uruchamia liczenie", aliases=["licz", "count"])
	async def liczenie(self, ctx, *, stringToParse=None):		
		if self.counting_channel_ID != 0:
			await ctx.send(f'Już utworzono kanał do liczenia: <#{self.counting_channel_ID}>')
			return
		
		if stringToParse is None:
			await ctx.send(f'Sprobuj `{str(ctx.message.content)} \'nazwa kanału do liczenia\'`')
		else:
			# '_' To tell the bot the channel already exists
			# and sending welcome embed isn't necessary 
			dont_sent_embed = False
			
			if stringToParse[0] == '_':
				stringToParse = stringToParse[1:]
				dont_sent_embed = True
				
			# Find channel_id by name
			for channel in ctx.guild.channels:
				if channel.name == stringToParse:
					self.counting_channel_ID = channel.id
					self.console(f'created counting channel on #{stringToParse}', ctx.author.display_name)
					await ctx.send(f'Kanał <#{channel.id}> został ustawiony jako kanał do liczenia!')
					
					info = discord.Embed(
						title='🤗 Liczenie!',
						description='Na tym kanale utworzono liczenie',
					)
					info.add_field(name='Zasady', value='• Liczymy od 1 w górę\n• Jedna osoba nie może wysłać wiadomości **dwa razy pod rząd**\n\n*Enjoy!*')

					if not dont_sent_embed:
						await channel.send(embed=info)
						
					await channel.edit(topic='To infinity and beyond!')

					# Autosave
					pins = await channel.pins()
					for m in pins:
						self.next_number = int(m.content) + 1
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


	@commands.command(brief="Ustawia aktualną liczbę", aliases=["setnumber"], hidden=True)
	async def ustawliczbe(self, ctx, *, stringToParse=None):
		if stringToParse is None or not stringToParse.isnumeric():
			await ctx.send(f'Użycie: `{str(ctx.message.content)} <dodatnia liczba całkowita>`')
			return
		next = int(stringToParse)
		self.next_number = next
		self.console('setting current number to {next}', ctx.author.display_name)
		await ctx.send(f'Ustawiono numer na **{next}**')

	@commands.command(brief="Sprawdza aktualna liczbe", aliases=["whatnum"], hidden=True)
	async def jakaliczba(self, ctx, *, stringToParse=None):
		await ctx.send(f'Kolejna liczba to **{self.next_number}**')
	
# Setup	
def setup(client):
	client.add_cog(Counter(client))
