import discord
from discord.ext import commands
from dotenv import load_dotenv

import os

# Load .env file
load_dotenv()

# Set a prefix for bot commands
client = commands.Bot(command_prefix='>')


@client.event
async def on_ready():
    print('Blathers, ready for action!')


# Test ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Run bot
client.run(os.environ['BOT_TOKEN'])