from __future__ import annotations

import discord
from discord.ext import commands
from res.misc import number_emojis


class Polls(commands.Cog):
    description = 'Automatyczne tworzenie ankiet'  # Required field
    qualified_name = "Ankiety"

    def __init__(self, client):
        self.client = client

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                     H E L P E R S                   # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @staticmethod
    def parse_mop_options(stringToParse: str) -> bool | (str, list[str], int | bool):
        fields = list(map(lambda string: string.strip(), stringToParse.split("&")))

        if len(fields) == 2:
            question, options = fields
            max_votes = False
        elif len(fields) == 3:
            question, options, max_votes = fields
            try:
                max_votes = int(max_votes)
                if max_votes <= 0:
                    max_votes = False
            except ValueError:
                return False
        else:
            return False

        return question, options, max_votes

    @staticmethod
    def console(msg, who='cog'):
        print(f'[{__class__.__name__}] {who}\t\t: {msg}')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                      E V E N T S                    # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @commands.Cog.listener()
    async def on_ready(self):
        self.console('is ready')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                    C O M M A N D S                  # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @commands.command(brief="Ankieta na tak, nie", aliases=["ynpoll"],
                      description="użycie: **$ynpoll** <pytanie>\nKomenda tworzy ankietę tak/nie na zadane pytanie.")
    async def YesNoPoll(self, ctx, *, question):
        await ctx.message.delete()
        poll = discord.Embed(title="Ankieta 📣", description=question, color=discord.Color.blue())
        poll.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        poll_message = await ctx.send(embed=poll)
        await poll_message.add_reaction('👍')
        await poll_message.add_reaction('👎')

    @commands.command(brief="Ankieta z wieloma odpowiedziami", aliases=["mopoll"],
                      description="użycie: **$mopoll** <pytanie> & <opcja1 | opcja2 | ...> [& max_votes]\nKomenda tworzy ankietę z możliwością wielokrotnego głosowania na zadane pytanie, z możliwością wybrania do max_votes wymienionych opcji.")
    async def MultipleOptionPoll(self, ctx, *, stringToParse):
        if self.parse_mop_options(stringToParse) is False:
            return
        await ctx.message.delete()

        question, options, max_votes = self.parse_mop_options(stringToParse)

        poll = discord.Embed(title="Ankieta 📣", description=question, color=discord.Color.blue())
        poll.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        options = list(set(options.split("|")))
        for option in options:
            poll.add_field(name=f"\u200b", value=f"{number_emojis[options.index(option) + 1]} {option}", inline=False)
        if max_votes:
            poll.set_footer(text=f"Głosujemy maksymalnie {max_votes} raz{'y' if max_votes > 1 else ''}!")

        poll_message = await ctx.send(embed=poll)

        for option in options:
            await poll_message.add_reaction(f"{number_emojis[options.index(option) + 1]}")


def setup(client):
    client.add_cog(Polls(client))
