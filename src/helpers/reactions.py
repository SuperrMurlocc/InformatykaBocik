async def limit_max_votes(reaction, user):
    embeds = reaction.message.embeds
    if len(embeds) == 0:
        return
    embed = embeds[0].to_dict()
    if 'title' not in embed:
        return
    if embed['title'] != "Ankieta 📣":
        return
    if 'footer' not in embed:
        return
    if not str(embed['footer']['text']).startswith("Głosujemy maksymalnie "):
        return
    max_votes = int(str(embed['footer']['text']).split()[2])
    user_reactions_count = 0
    for _reaction in reaction.message.reactions:
        async for _user in _reaction.users():
            if user == _user:
                user_reactions_count += 1
    if user_reactions_count > max_votes:
        await reaction.remove(user)
        await user.send(f"Hej, w tej ankiecie głosujemy tylko {max_votes} raz(y). Aby zmienić głos, wpierw usuń inną reakcję.")