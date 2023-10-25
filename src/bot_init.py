from discord.ext import commands
import discord


def init():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(
        command_prefix="!",  # Change to desired prefix
        case_insensitive=True, # Commands aren't case-sensitive
        intents = intents # Set up basic permissions
    )

    bot.author_id = 198544375926620160  # Change to your discord id

    return bot
