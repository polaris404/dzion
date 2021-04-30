import discord
from discord.ext import commands
from utils.constants import COLOURS


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        bot = await self.client.application_info()
        e = discord.Embed(title=f"{bot.name} Commands!",
                          description=f'Here is the list of commands by Categories\nCurrent prefix is `_`', colour=COLOURS['purple'])
        e.add_field(name='__Todo Commands__ :tools:', value=f'`todo[td]` : Give a list of things todo\n`todo[td] add *task* <time>` : Add task to ToDo list.\n`todo[td] remove *index*` : Removes the task at *index* from the ToDo list.\n`todo remove all` removes all tasks', inline=False)
        e.set_thumbnail(url=str(bot.icon_url))
        e.set_footer(text="<> indicates optional|[] indicates aliases of that command")
        e.add_field(name='__Extra__ :linked_paperclips:', value=f'`about` : To know more about the bot\n`invite` : Get the invite link\n`info` : Get info of bot\n`userinfo <user>` : Gives info of user', inline=False)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Help(client))
