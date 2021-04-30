import discord
import pathlib
from discord.ext import commands
from utils import constants
import sys
import traceback

PREFIX = constants.DEFAULT_PREFIX
print(PREFIX)


class DZion(commands.Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        # self.OWNER = OWNER
        # self.ADMINS = ADMINS
        # self.GUILD = BOT_GUILD

        self.ready = False

        self.bot_intents = discord.Intents(
            guilds=True,
            members=True,
            emojis=True,
            presences=True,
            messages=True,
            dm_messages=True,
            reactions=True,
        )
        super().__init__(command_prefix=PREFIX, intents=self.bot_intents)

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot Disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("Bot is ready")
        else:
            print("Bot reconnected")


client = DZion()
client.remove_command("help")

modules = [f"{p.parent}.{p.stem}" for p in pathlib.Path("./cogs").rglob("*.py")]
failed = []
for extension in modules:
    try:
        client.load_extension(extension)
        print(extension + " Loaded")
    except Exception as e:
        failed.append(f"{extension}: {e}")
        print(f"Failed to load extension <{extension}>.", file=sys.stderr)
        traceback.print_exception(etype=type(e), tb=e.__traceback__, value=e)

if failed:
    print(
        "\n\nThe following extensions failed to load:\n{}\n".format(
            "\n".join(f for f in failed)
        )
    )
else:
    print("All Cogs Loaded")


client.run(constants.TOKEN)
