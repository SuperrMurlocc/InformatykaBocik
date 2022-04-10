import os
import discord
from discord.ext import commands

from src.keep_alive import keep_alive
from src.secrets import load_secrets, get_secret

from datetime import date

import logging
from src.format import JSONFormatter

# Creates debug .json file containing all managed events 
DEBUG_MODE = True
LOG_PATH = 'log/'

load_secrets()
TOKEN = get_secret('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="$", intents=intents)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # #              G L O B A L   E V E N T S              # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@client.event
async def on_ready():
	for guild in client.guilds:
		
		print(
			f'discord.py {discord.__version__} \n'
			f'{client.user} is connected to the following guild: \n'
			f'{guild.name} (id: {guild.id})'
		)

		print("Guild Members:")
		for member in guild.members:
			print(f'- {member.name}')
	
		# Create logging directory
		if DEBUG_MODE: # Create logging directory
			configure_logging();

	
	await client.change_presence(activity=discord.Game("On Host"))


@client.event
async def on_member_join(member):
	channel_to_welcome = discord.utils.get(member.guild.channels, id="?")
	message = discord.Embed(title=f"Witaj {member.mention}!",
							color=discord.Color.green(),
							description=f"Fajnie, że wpadłeś! Zacznij od ustawienia sobie nicku, tak, aby w nawiasie było twoje imię i nazwisko."
										f"\nNapisz również poniżej czy jesteś ze starszego czy młodszego rocznika - jeden z naszych administratorów "
										f"odszuka Cię i potwierdzi, że nie jesteś dziekanem.")
	await channel_to_welcome.send(embed=message)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # #             E R R O R   H A N D L I N G             # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		message = discord.Embed(title=f"Nie mam takiej komendy!", color=discord.Color.red())
		await ctx.send(embed=message)

@client.event
async def on_error(event, *args):
	with open('log/err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

def configure_logging():
	if not os.path.exists(LOG_PATH):
		os.makedirs(LOG_PATH)
		print(f"Created {LOG_PATH} directory")

	sessionID = date.today().strftime("%d-%m-%Y-") + str(os.getpid()) + '.json'
	
	name = LOG_PATH + 'log-' + sessionID
	logger = logging.getLogger('discord')
	logger.setLevel(logging.DEBUG)
	logger.addFilter(NoParsingFilter())
	handler = logging.FileHandler(filename=name, encoding='utf-8', mode='w')
	handler.setFormatter(JSONFormatter())
	logger.addHandler(handler)
	

class NoParsingFilter(logging.Filter):
	# TODO: Fix this filter to only display relevant messages
    def filter(self, record):
        return record.getMessage().contains('WebSocket Event') or record.getMessage().startsWith('POST')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # #                     M O D U L E S                   # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@client.command(brief="Ładuje moduł")
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
	client.load_extension(f'src.cogs.{extension}')


@client.command(brief="Usuwa moduł")
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
	client.unload_extension(f'src.cogs.{extension}')


@client.command(brief="Przeładowuje moduł")
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
	client.unload_extension(f'src.cogs.{extension}')
	client.load_extension(f'src.cogs.{extension}')


for filename in os.listdir("./src/cogs"):
	if filename.endswith('.py'):
		client.load_extension(f'src.cogs.{filename[:-3]}')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # #                          R U N                      # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# keep_alive()
client.run(TOKEN)
