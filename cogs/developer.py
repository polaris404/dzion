import discord
from discord.ext import commands
from time import time
from psutil import Process
from datetime import timedelta, datetime, date
from utils import checks
from utils.constants import COLOURS
from utils.texttime import timetotext


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @checks.private_command()
    async def ping(self, ctx):
        e = discord.Embed(colour=COLOURS['black'])
        e.add_field(name="Ping", value=f'{round(self.client.latency*1000)}ms', inline=False)
        start = time()
        msg = await ctx.send(embed=e)
        end = time()
        e.add_field(name="Response Time", value=f'{round((end-start)*1000)}ms')
        await msg.edit(embed=e)

    @commands.command()
    @checks.private_command()
    async def cogs(self, ctx):
        all_cogs = '\n'.join(self.client.cogs.keys())
        e = discord.Embed(title="Loaded Cogs",
                          description=f'```{all_cogs}```', colour=COLOURS['black'])
        await ctx.send(embed=e)

    @commands.command()
    @checks.private_command()
    async def intents(self, ctx):
        intents_list = []
        for i, bool in list(self.client.intents):
            if bool:
                intents_list.append(":white_check_mark: : " + i)
            else:
                intents_list.append(":x: :" + i)
        e = discord.Embed(title="Intents", description='\n'.join(
            intents_list), colour=COLOURS['black'])
        await ctx.send(embed=e)

    @commands.command()
    @checks.private_command()
    async def uptime(self, ctx):
        proc = Process()
        with proc.oneshot():
            up_time = timedelta(seconds=time() - proc.create_time())
        e = discord.Embed(colour=COLOURS['black'])
        e.add_field(name="Uptime", value=f"{timetotext(up_time)}", inline=False)
        e.add_field(name="Started On",
                    value=f'{(date.today() - up_time).strftime("%d %B, %Y")} at {datetime.fromtimestamp(proc.create_time()).strftime("%H:%M:%S")}')
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Dev(client))
