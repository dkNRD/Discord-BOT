# Imports
import bot_init
import discord
import commands
import events

# Bot init
bot = bot_init.init()


# Events handlers
@bot.event
async def on_ready():  # When the bot is ready
    events.on_ready(bot)


@bot.event
async def on_message(ctx):
    await commands.on_message(ctx, bot)


# Commands handlers
@bot.command()
async def pong(ctx):
    await commands.pong(ctx)


@bot.command()
async def name(ctx):
    await commands.name(ctx)


@bot.command()
async def d6(ctx):
    await commands.d6(ctx)


@bot.command()
async def admin(ctx, member: discord.Member):
    await commands.admin(ctx, member)


@bot.command()
async def ban(ctx, member: discord.Member, reason: str):
    await commands.ban(ctx, member, reason)


@bot.command()
async def flood(ctx, message):
    await commands.flood(ctx, message)


# Bot runner
token = "MTE2Njc4NDUyNTU1NzMwMTI5OA.GcBzng.5cIEkAFKuNqM15rB1KOJAqGfLvJf-LszTvq_64"
bot.run(token)  # Starts the bot
