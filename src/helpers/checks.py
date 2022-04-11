from src.helpers.secrets import get_secret


def check_guild(ctx) -> bool:
    return str(ctx.guild.id) == get_secret('GUILD')
