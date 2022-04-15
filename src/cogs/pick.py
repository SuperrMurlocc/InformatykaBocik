import discord
from discord.ext import commands
import random
import secrets
import discord.utils

class RandomPicker(commands.Cog):
	description = 'Wybiera jedną osobę w obrębie danej roli' # Required field
	qualified_name = "Losowanie"
	
	def __init__(self, client):
		self.client = client

	# Helpers
	@staticmethod
	def console(msg, who='cog'):
		print(f'[{__class__.__name__}] ({who})\t: {msg}')

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		self.console('is ready')

	# Commands
	@commands.command(brief="Losuje osobę", aliases=["losowanie", "pick", "wybierz"])
	async def losuj(self, ctx, role:discord.Role=None):
		if role is None:
			await ctx.send(embed=discord.Embed(
				color = discord.Color.blue(),
				description = f'**Aby wylosować wpisz `{ctx.message.content} \'nazwa grupy\'`**'
			))
			return
			
		random_member = secrets.choice(role.members)
		while random_member.bot:
			random_member = random.choice(role.members)
			
		group = ''
		if role.name[0] != '@':
			group = '@' + role.name
		else:
			group = role.name
			
		info = discord.Embed(
			title = f'Losowanie z grupy {group}',
			color = discord.Color.teal(),
			description = f':point_right: **{random_member.display_name}**\n\n*losowanie na prośbę {ctx.message.author.display_name}*'
		)

		info.set_thumbnail(url = random_member.avatar_url)
		await ctx.message.delete()
		await ctx.send(embed = info)


def setup(client):
	client.add_cog(RandomPicker(client))
