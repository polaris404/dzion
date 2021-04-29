from datetime import timedelta
from time import time
from sys import version_info
import discord
from discord.ext import commands
from utils.constants import COLOURS, BOT_VERSION
from psutil import Process, virtual_memory


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        e = discord.Embed(title=f'User : {user}',
                          color=COLOURS['purple'], timestamp=ctx.message.created_at)
        e.add_field(name="Nickname", value=f'{user.display_name}', inline=False)
        e.add_field(name="User ID", value=f'{user.id}', inline=False)
        e.add_field(name="Top Role", value=f'{user.top_role.mention}', inline=True)
        e.add_field(name="Status", value=f'{user.status}', inline=True)
        e.add_field(name="Bot", value=f'{user.bot}', inline=True)
        e.add_field(name="Joined", value=user.joined_at.strftime(
            "On %d/%m/%Y at %H:%M:%S UTC"), inline=False)
        e.add_field(name="Created", value=user.created_at.strftime(
            "On %d/%m/%Y at %H:%M:%S UTC"), inline=False)
        e.set_thumbnail(url=user.avatar_url)
        e.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def info(self, ctx):
        bot = await self.client.application_info()
        e = discord.Embed(title=f"{bot.name}",
                          description=f"{bot.description}", colour=COLOURS['purple'])
        e.add_field(name="Latency", value=f"{round(self.client.latency*1000)}ms")
        e.add_field(name="Guilds", value=f'{len(self.client.guilds)}')
        e.add_field(name="Prefix", value=f'`_`')
        e.add_field(name="Author", value=f'{bot.owner}')
        e.add_field(name="Invite URL",
                    value=f'[Invite Link](https://discord.com/api/oauth2/authorize?client_id=760739125044969472&permissions=8&scope=bot)')
        e.set_thumbnail(url=str(bot.icon_url))
        e.set_footer(
            text=f'Python Version - {version_info.major}.{version_info.minor}.{version_info.micro} | Discord.py Version - {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro}')
        await ctx.send(embed=e)

    @commands.command()
    async def advinfo(self, ctx):
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time() - proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)
        bot = await self.client.application_info()
        e = discord.Embed(title=f"{bot.name}",
                          description=f"{bot.description}", colour=COLOURS['purple'])
        e.add_field(name="Bot Version", value=f'{BOT_VERSION}', inline=False)
        e.add_field(name="Uptime", value=f'{str(uptime).split(".")[0]}', inline=True)
        e.add_field(name="‍", value="‍")
        e.add_field(name="CPU time", value=f'{str(cpu_time).split(".")[0]}', inline=True)

        # name and value of below field are Zero Width Space not empty
        # Check this : https://emojipedia.org/zero-width-joiner/
        e.add_field(name="Ping", value=f'{round(self.client.latency*1000)}ms', inline=True)
        e.add_field(name="‍", value="‍")
        e.add_field(name="Response Time", value=f'-', inline=False)
        e.add_field(name="Memory Usage", value=f'{mem_usage:,.0f}/{mem_total:,.0f} MB', inline=True)
        e.add_field(name="Memory Usage %", value=f'{mem_of_total:,.2f}%', inline=True)
        e.set_thumbnail(url=str(bot.icon_url))
        e.set_footer(
            text=f'Python Version - {version_info.major}.{version_info.minor}.{version_info.micro} | Discord.py Version - {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro}')
        start = time()
        msg = await ctx.send(embed=e)
        end = time()
        e.set_field_at(index=6, name="Response Time",
                       value=f'{round((end-start)*1000)}ms', inline=True)
        await msg.edit(embed=e)

    @commands.command()
    async def serverinfo(self, ctx):
        e = discord.Embed(title=f"{ctx.guild.name}",
                          colour=COLOURS['purple'], timestamp=ctx.message.created_at)
        e.add_field(name="Owner", value=f'{ctx.guild.owner}')
        e.add_field(name="Created at", value=ctx.guild.created_at.strftime(
            "On %d/%m/%Y at %H:%M:%S UTC"), inline=False)
        e.add_field(name="Roles", value=f'{len(ctx.guild.roles)}')
        e.add_field(name="Members", value=f'{ctx.guild.member_count}')
        e.add_field(name="Guild ID", value=f'{ctx.guild.id}')
        e.add_field(name="Shard ID", value=f'{ctx.guild.shard_id}')
        e.add_field(
            name="Channels", value=f'Text Channels : {len(ctx.guild.text_channels)}\nVoice Channels : {len(ctx.guild.voice_channels)}')
        e.set_thumbnail(url=str(ctx.guild.icon_url))
        e.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def invite(self, ctx):
        bot = await self.client.application_info()
        e = discord.Embed(title=f"{bot.name}'s Invite Url",
                          description=f"[Invite link](https://discord.com/api/oauth2/authorize?client_id=809083240128315402&permissions=8&scope=bot)", colour=COLOURS['purple'])
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Info(client))
