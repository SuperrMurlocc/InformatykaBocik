import os
import discord
from discord.ext import commands

from src.helpers.keep_alive import keep_alive
from src.helpers.secrets import load_secrets, get_secret
from src.helpers.reactions import limit_max_votes

# Creates debug .json file containing all managed webbooks
LOGGING_MODE = True
if LOGGING_MODE:
    from src.helpers.logger import *

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
        if LOGGING_MODE:  # Create logging directory
            configure_logging()

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


@client.event
async def on_reaction_add(reaction, user):
    if user.name == "ZajebistyBot":
        return
    if reaction.message.author.name != "ZajebistyBot":
        return

    await limit_max_votes(reaction, user)


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
