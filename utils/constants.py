import json
import discord
import os

TOKEN = os.getenv('Token')

DEFAULT_PREFIX = '_'
OWNER = 629712906011017256
ADMINS = [629712906011017256]
BOT_VERSION = "v1.0.0"
GUILD = 756415045981831188
CHANNELS = {
    "issues": 767336325647958046,
    "suggestions": 767284237282836520,
    "errors": None
}

COLOURS = {
    "purple": discord.Colour(0xf0d389),
    "black": discord.Colour(0x16161D),
    "red": discord.Colour(0xf7561b)
}
