import discord
import os
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    description = 'Wyświetla pomoc'  # Required field

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):

        ctx = self.context

        await ctx.message.delete()  # Delete user message
        helpmsg = discord.Embed(
            color=discord.Color.magenta(),
        )

        # Check if the user is on mobile phone
        member = ctx.guild.get_member_named(ctx.author.name)
        if member.is_on_mobile():
            for cog in mapping:
                cmds = ""

                for command in mapping[cog]:
                    if command.name == 'help':
                        continue
                    cmds += f'\n`{command.name}` - {command.brief}'

                if cog is not None:
                    helpmsg.add_field(name=f'{cog.qualified_name}', value=f'{cmds}')
                else:
                    helpmsg.add_field(name=f'**Pozostałe komendy**', value=f'{cmds}')
        else:
            for cog in mapping:
                cmds = ""
                briefs = ""
                for command in mapping[cog]:
                    if command.name == 'help':
                        continue
                    cmds += f'`{command.name}`\n\u200b'
                    briefs += f'{command.brief}\n\u200b'

                if cog is not None:
                    helpmsg.add_field(name=f'{cog.qualified_name}', value=cmds)
                    helpmsg.add_field(name=f'*{cog.description}*', value=briefs)
                    helpmsg.add_field(name='\u200b', value='\u200b')
                else:
                    helpmsg.add_field(name=f'**Pozostałe komendy**', value=cmds)
                    helpmsg.add_field(name=f'*Robią inne ciekawe rzeczy*', value=briefs)
                    helpmsg.add_field(name='\u200b', value='\u200b')

        helpmsg.add_field(name=f'*Aby uzyskać pomoc dla danej komendy wpisz:*  `{ctx.message.content} <komenda>`',
                          value='\u200b')
        helpmsg.set_footer(text=f'utworzono na prośbę {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=helpmsg)

    async def send_cog_help(self, cog):
        print("COG", cog)
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        print("GROUP", group)
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        await self.context.message.delete()

        if command.description:
            helpmsg = discord.Embed(title=f"**${command}**", description=f'{command.description}',
                                    color=discord.Colour.blue())
            helpmsg.set_footer(text=f'utworzono na prośbę {self.context.author.display_name}',
                               icon_url=self.context.author.avatar_url)
            return await self.context.send(embed=helpmsg)
        else:
            helpmsg = discord.Embed(title="Sory...",
                                    description=f"{command} nie ma wypełnionego opisu szczegółowego :/",
                                    color=discord.Colour.red())
            helpmsg.set_footer(text=f'utworzono na prośbę {self.context.author.display_name}',
                               icon_url=self.context.author.avatar_url)
            return await self.context.send(embed=helpmsg)
