import discord
from discord.ext import commands
from utils import constants


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def suggest(self, ctx, *, text):
        CHANNEL = self.client.get_channel(constants.CHANNELS['suggestions'])
        e = discord.Embed(colour=constants.COLOURS['purple'], timestamp=ctx.message.created_at)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(
            name="Info", value=f'Author ID : {ctx.author.id}\nGuild : {ctx.guild.name}({ctx.guild.id})', inline=False)
        e.add_field(name="Suggestion:", value=f'{text}')
        msg = await CHANNEL.send(embed=e)
        await msg.add_reaction("\U00002705")
        await msg.add_reaction("\U0000274c")
        await ctx.message.add_reaction("\U0001f4ec")

    @commands.command()
    async def issue(self, ctx, *, text):
        CHANNEL = self.client.get_channel(constants.CHANNELS['issues'])
        e = discord.Embed(colour=constants.COLOURS['purple'], timestamp=ctx.message.created_at)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(
            name="Info", value=f'Author ID : {ctx.author.id}\nGuild : {ctx.guild.name}({ctx.guild.id})', inline=False)
        e.add_field(name="Issue:", value=f'{text}')
        msg = await CHANNEL.send(embed=e)
        await msg.add_reaction("\U00002705")
        await msg.add_reaction("\U0000274c")
        await ctx.message.add_reaction("\U0001f4ec")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        admins = constants.ADMINS
        CHANNELS = [constants.CHANNELS['issues'], constants.CHANNELS['suggestions']]
        if payload.user_id in admins and payload.channel_id in CHANNELS:
            CHANNEL = self.client.get_channel(payload.channel_id)
            if payload.emoji.name == "✅":
                msg = await CHANNEL.fetch_message(payload.message_id)
                await msg.clear_reactions()
            elif payload.emoji.name == '❌':
                msg = await CHANNEL.fetch_message(payload.message_id)
                await msg.delete()


def setup(client):
    client.add_cog(Misc(client))
