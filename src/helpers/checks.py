from src.helpers.secrets import get_secret


def check_guild(ctx) -> bool:
    return str(ctx.guild.id) == get_secret('GUILD')


def check_is_student(ctx) -> bool:
    return 761153698612903967 in ctx.author.roles()
