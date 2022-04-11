from __future__ import annotations
import discord


def is_ankieta(reaction) -> bool:
    embeds = reaction.message.embeds
    if len(embeds) == 0:
        return False
    embed = embeds[0].to_dict()
    if 'title' not in embed:
        return False
    if embed['title'] != "Ankieta 📣":
        return False
    return True


async def limit_votes(reaction, user) -> bool:
    embed = reaction.message.embeds[0].to_dict()
    if 'footer' not in embed:
        return False
    if not str(embed['footer']['text']).startswith("Głosujemy maksymalnie "):
        return False
    max_votes = int(str(embed['footer']['text']).split()[2])
    user_reactions_count = 0
    for _reaction in reaction.message.reactions:
        async for _user in _reaction.users():
            if user == _user:
                user_reactions_count += 1
    if user_reactions_count > max_votes:
        await reaction.remove(user)
        await user.send(f"Hej, w tej ankiecie głosujemy tylko {max_votes} raz(y). Aby zmienić głos, wpierw usuń inną reakcję.")
        return False
    return True


def fields_has_name_progress_bar(fields: list) -> bool | int:
    i = 0
    for field in fields:
        if field['name'] == 'Postęp:':
            return i
        i += 1
    return False


def progress_bar_message(reactions: list) -> dict[str, str | bool]:
    all_votes = sum([count for _, count in reactions])
    message = f"Głosów łącznie: {all_votes}\n\n"
    message += "\n\n".join([
        f"{reaction}: {count}|{'█' * ((16*count)//all_votes)}{'░'  * (16 - (16*count)//all_votes)}|{(count*100)//all_votes}%"
        for reaction, count in reactions if count != 0])
    return {'name': 'Postęp:', 'value': message, 'inline': False}


async def progress_bar(reaction):
    embed = reaction.message.embeds[0].to_dict()
    reactions = [(_reaction, _reaction.count - 1) for _reaction in reaction.message.reactions]
    if 'fields' not in embed:
        embed['fields'] = []
    _f = fields_has_name_progress_bar(embed['fields'])
    if _f is not False:
        embed['fields'][_f] = progress_bar_message(reactions)
    else:
        embed['fields'].append(progress_bar_message(reactions))
    await reaction.message.edit(embed=discord.Embed.from_dict(embed))
