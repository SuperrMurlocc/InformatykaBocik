import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import os
import pickle

class Eggs(commands.Cog):
	description = 'Wielkanocna gra w zbieranie jajek' # Required field
	qualified_name = "Egg hunt"
	
	egg_hunt_channel_ID = int(0)
	CHANNEL_NAME = 'zbieranie-jajek'
	cooldown_time = 0
	red = []
	blue = []
	points = {}
	all_eggs_available = 0
	red_eggs = 0
	blue_eggs = 0
	
	def __init__(self, client):
		self.client = client

	# Helpers
	@staticmethod
	def console(msg, who='cog'):
		print(f'[{__class__.__name__}] {who}\t\t: {msg}')

	@staticmethod
	def are_teams_saved():
		return os.path.exists('res/egg_progress.pkl')
	
	@staticmethod
	def save_teams(red, blue, points, all, rde, ble):
		with open('res/egg_progress.pkl', 'wb+') as f:
			pickle.dump(red, f)
			pickle.dump(blue, f)
			pickle.dump(points, f)
			pickle.dump(all, f)
			pickle.dump(rde, f)
			pickle.dump(ble, f)
		return 'saved teams to file in res/'

	@staticmethod
	def load_teams():
		red = []
		blue = []
		points = {}
		eggs = 0
		red_e = 0
		blue_e = 0
		
		with open('res/egg_progress.pkl', 'rb') as f:
			red = pickle.load(f)
			blue = pickle.load(f)
			points = pickle.load(f)
			eggs = pickle.load(f)
			red_e = pickle.load(f)
			blue_e = pickle.load(f)
		return red, blue, points, eggs, red_e, blue_e

	@staticmethod
	def remove_teams():
		os.remove('res/egg_progress.pkl')
		
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		self.console('is ready')
				
	# Commands
	@has_permissions(administrator=True)
	@commands.command(brief="Uruchamia grę w zbieranie jajek", aliases=["eggs"])
	async def jaja(self, ctx):
		# Check if there is progress already saved
		if self.are_teams_saved():
			self.red, self.blue, self.points, self.all_eggs_available, self.red_eggs, self.blue_eggs = self.load_teams()
			
			self.console('loaded saved teams from file')
			
		else:
			# Divide guild members into 2 teams
			players = []
			for member in ctx.guild.members:
				if member.bot is False:
					players.append(member.id)
	
			self.points = {i : 0 for i in players}
			# self.points = dict.fromkeys(players , 0)
			random.shuffle(players)
		
			dp = int(len(players)/2)
			self.red = players[:dp]
			self.blue = players[dp:]
			self.all_eggs_available = random.randint(10000, 20000)
			self.red_eggs = 0
			self.blue_eggs = 0
			self.save_teams(self.red, self.blue, self.points, self.all_eggs_available, self.red_eggs, self.blue_eggs)
			self.console('saved teams to file')

		# Create egg game channel if missing
		if not any(self.CHANNEL_NAME in channel.name for channel in ctx.guild.channels):
			new_channel = await ctx.guild.create_text_channel(self.CHANNEL_NAME)
			self.egg_hunt_channel_ID = new_channel.id
			
			info = discord.Embed(title='Gra w zbieranie jajek wystartowała', description='Ten kanał to wielkie zielone pole, na którym zostały poukrywane **jaja wielkanocne**. Szukaj ukrytych jaj, aby zdobyć **punkty** dla twojej drużyny')
			info.add_field(name='Zasady', value=f'• Aby poświęcić swój czas na szukanie, użyj komendy `{ctx.prefix}szukaj`\n• Jaja są bardzo dobrze poukrywane, więc może się zdarzyć, że nie znajdziesz ani jednego\n• Szukanie jaj kosztuje energię, więc zanim będziesz mógł szukać po raz kolejny musisz odczekać **{self.cooldown_time} minut**', inline=False)
			info.add_field(name='Drużyny', value=f'• Jesteście podzieleni na dwie drużyny:\n🔵 **TEAM BLUE**\n🔴 **TEAM RED**\n• Aby zobaczyć, w której drużynie jesteś użyj `{ctx.prefix}team`\n• Aby zobaczyć jak wam idzie, użyj `{ctx.prefix}status`\n• **Liczba jajek jest ograniczona**, gra zakończy się w momencie, gdy znajdziecie wszystkie z nich**\n\n*Enjoy!*', inline=False)
			info.set_image(url='https://static1.makeuseofimages.com/wordpress/wp-content/uploads/2022/03/Bright-colorful-Easter-eggs-and-rabbit-ears-on-a-blue-and-wooden-background-with-green-moss.jpg?q=50&fit=contain&w=767&h=384&dpr=1.5')
			await new_channel.send(embed=info)
			await new_channel.edit(topic='Let\'s find them all!')
			await ctx.channel.send(f'Utworzono kanał do szukania jajek wielkanocnych w <#{self.egg_hunt_channel_ID}>')
			self.console(f'created egg hunt channel (id: {self.egg_hunt_channel_ID})', ctx.author)
		else:
			ch = discord.utils.get(ctx.guild.channels, name=self.CHANNEL_NAME)
			self.egg_hunt_channel_ID = ch.id
			await ctx.channel.send(f'Kanał jest już utworzony w <#{self.egg_hunt_channel_ID}>')

	@commands.command(brief="Sprawdzanie swojej drużyny")
	async def team(self, ctx):
		await ctx.message.delete()
		em = discord.Embed()
		if ctx.author.id in self.red:
			em.add_field(name=f'{ctx.author.display_name} 🥚: {self.points[ctx.author.id]}', value='🔴 **TEAM RED** 🔴')
		elif ctx.author.id in self.blue:
			em.add_field(name=f'{ctx.author.display_name} 🥚: {self.points[ctx.author.id]}', value='🔵 **TEAM BLUE** 🔵')
		else:
			em.add_field(name=f'{ctx.author.display_name}', value='**Gra w zbieranie jajek nie została reszcze rozpoczęta**')
		await ctx.send(embed=em)
		
		
	@commands.command(brief="Komenda do szukania jajek")
	@commands.cooldown(1, cooldown_time * 60, commands.BucketType.user)
	async def szukaj(self, ctx):
		await ctx.message.delete()
		if ctx.channel.id != self.egg_hunt_channel_ID or self.all_eggs_available == 0:
			return

		if random.random() < random.uniform(0.3, 0.8):
			self.all_eggs_available -= 1
			self.points[ctx.author.id] += 1
			team = ''
			if ctx.author.id in self.red:
				team = '🔴'
				self.red_eggs += 1
			elif ctx.author.id in self.blue:
				team = '🔵'
				self.blue_eggs += 1
			
			em = discord.Embed(title=f'{team} Znalazłeś(aś) jajo!', description=f'liczba znalezionych przez Ciebie jaj: `{self.points[ctx.author.id]}`', color = discord.Color.gold())
			em.set_thumbnail(url = 'https://img.freepik.com/free-vector/cute-happy-chicken-egg-cartoon-character-chicken-egg-easter-concept_92289-1205.jpg?w=826')
			em.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em)
		else:
			em = discord.Embed(description=f"**Niestety, tym razem nic nie znalazłeś/aś**\n*Ale możesz spróbować ponownie za `{self.cooldown_time}` minut*")
			em.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em)
		if self.all_eggs_available == 0:
			winner = '!!! *REMIS* !!!'
			if self.red_eggs > self.blue_eggs:
				winner = '🔴 Wygrywa **TEAM RED** 🔴'
			elif self.blue_eggs > self.red_eggs:
				winner = '🔵 Wygrywa **TEAM BLUE** 🔵'
			endgame = discord.Embed(title=f'{winner}!', description=f'liczba znalezionych przez was jaj 🥚 : `{self.red_eggs + self.blue_eggs}`')
			endgame.set_image(url='https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F24%2F2022%2F03%2F28%2FGettyImages-137813261-2000.jpg&q=60')
			endgame.add_field(name='\u200b', value='Dziękujemy wszystkim za udział w grze!')
			await ctx.send(embed=endgame)

			
	@szukaj.error
	async def command_name_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.message.delete()
			em = discord.Embed(description=f"Możesz spróbować ponownie za {error.retry_after:.2f} sekund")
			em.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em)

		
	@has_permissions(administrator=True)
	@commands.command(brief="Usuwa drużyny", hidden=True)
	async def removeteams(self, ctx):
		self.remove_teams()
		self.console('removed saved teams')
		await ctx.send('Usunięto zapisane drużyny.')

		
	@commands.command(brief="Zapisuje obecny postęp gry")
	async def saveeggs(self, ctx):
		self.save_teams(self.red, self.blue, self.points, self.all_eggs_available, self.red_eggs, self.blue_eggs)
		self.console('saved progress')
		await ctx.send('Zapisano postęp!')

	@commands.command(brief="Wyświetla obecny postęp drużyn")
	async def status(self, ctx):
		await ctx.message.delete()
		r = self.red_eggs
		b = self.blue_eggs
		all_votes = r + b
		if all_votes == 0:
			await ctx.send('Nikt jeszcze nie zaczął szukać jajek!')
			return
		msg = f"Razem zebraliście 🥚 : {all_votes}\n\n"
		rbar = f"🔴\t| {'█' * ((16*r)//all_votes)}{'░'  * (16 - (16*r)//all_votes)}|{(r*100)//all_votes}%"
		
		bbar = f"🔵\t| {'█' * ((16*b)//all_votes)}{'░'  * (16 - (16*b)//all_votes)}|{(b*100)//all_votes}%"
		
		em = discord.Embed(description=msg)
		em.add_field(name='TEAM RED', value=rbar, inline=False)
		em.add_field(name='TEAM BLUE', value=bbar, inline=False)
		await ctx.send(embed=em)

	@has_permissions(administrator=True)
	@commands.command(brief="Wyświetla obecny stan gry (debug)", aliases = ['eggstatus', 'eggcount'], hidden=True)
	async def eggstate(self, ctx):
		em = discord.Embed(description=f'RED: {self.red}\nBLUE:{self.blue}\nEGGS:{self.all_eggs_available}\nRED EGGS: {self.red_eggs}\nBLUE EGGS: {self.blue_eggs}')
		await ctx.send(embed=em)

	@has_permissions(administrator=True)
	@commands.command(brief="Pozwala na zmianę liczby jaj", hidden=True)
	async def force(self, ctx, amount):
		if amount is None:
			return await ctx.send('Please provide an amount')
		try:
			self.all_eggs_available = int(amount)
		except ValueError:
			await ctx.send(f'{amount} is not an integer!')
		await ctx.send(f'new egg count: {self.all_eggs_available}')
		
# Setup	
def setup(client):
	client.add_cog(Eggs(client))
