from discord.ext import commands
from utils import constants
# from services import ConfigService


def private_command():
    async def predicate(ctx):
        if ctx.author.id not in constants.ADMINS:
            raise commands.CheckFailure("You can't use this command")
        else:
            return True

    return commands.check(predicate)

