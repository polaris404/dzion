import sys
import discord
import pathlib
from discord.ext import commands
from utils.constants import COLOURS
from utils import checks
import traceback


class LoadCogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @checks.private_command()
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f'cogs.{extension}')
            e = discord.Embed(title=f"cog.{extension} has been loaded", colour=COLOURS['black'])
            await ctx.send(embed=e)
        except Exception:
            await ctx.send("*Extension already loaded or Not Available*")

    @commands.command()
    @checks.private_command()
    async def unload(self, ctx, extension):
        try:
            if extension != 'loadcogs':
                self.client.unload_extension(f'cogs.{extension}')
                e = discord.Embed(
                    title=f"cog.{extension} has been removed", colour=COLOURS['black'])
                await ctx.send(embed=e)
        except Exception:
            await ctx.send("*Extension already unloaded or Not Available*")

    @commands.command(aliases=['re'])
    @checks.private_command()
    async def reload(self, ctx, ext=None):
        r_cogs_list = []
        modules = [f'{p.parent}.{p.stem}' for p in pathlib.Path("./cogs").rglob('*.py')]
        modules.remove('cogs.loadcogs')
        failed = []
        if ext is None:
            for extension in modules:
                try:
                    self.client.unload_extension(extension)
                    self.client.load_extension(extension)
                    r_cogs_list.append(":white_check_mark: " + extension)
                except Exception as e:
                    failed.append(f'{extension}: {e}')
                    print(f'Failed to load extension <{extension}>.', file=sys.stderr)
                    traceback.print_exception(etype=type(e), tb=e.__traceback__, value=e)
                    r_cogs_list.append(":x: " + extension)

            r_cogs = "\n".join(r_cogs_list)
            e = discord.Embed(title="Reloaded Cogs",
                              description=f'{r_cogs}', colour=COLOURS['black'])
            await ctx.send(embed=e)
        else:
            extension = "cogs." + ext
            if extension in modules:
                try:
                    self.client.unload_extension(extension)
                    self.client.load_extension(extension)
                    e = discord.Embed(
                        title=f":white_check_mark: {extension} Reloaded", colour=COLOURS['black'])
                    await ctx.send(embed=e)
                except Exception as e:
                    e = discord.Embed(
                        title=f":x: {extension} failed to reload", colour=COLOURS['black'])
                    await ctx.send(embed=e)
                    failed.append(f'{extension}: {e}')
                    print(f'Failed to load extension <{extension}>.', file=sys.stderr)
                    traceback.print_exception(etype=type(e), tb=e.__traceback__, value=e)


def setup(client):
    client.add_cog(LoadCogs(client))
