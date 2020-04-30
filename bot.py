import discord
from discord.ext import commands
from dotenv import load_dotenv

import os, json

from helpers.serversettings import Serversettings


# Load .env file
load_dotenv()

# Load custom server settings
def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or('>')(bot, message)
    
    serversettings = Serversettings().load()

    guild_id = str(message.guild.id)    
    if guild_id not in serversettings or 'prefix' not in serversettings[guild_id]:
        return commands.when_mentioned_or('>')(bot, message)

    prefix = serversettings[guild_id]['prefix']
    return commands.when_mentioned_or(prefix)(bot, message)


# Set a prefix for bot commands
bot = commands.Bot(command_prefix=get_prefix, owner_id=228179496807694336)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Blathers, ready for action!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("I'm afraid that command does not exist.")
    elif isinstance(error, discord.ext.commands.errors.TooManyArguments):
        await ctx.send("Calm down there! You're giving me WAY too many arguments for that command!")
    else:
        raise error


# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Run bot
if __name__ == '__main__':
    bot.run(os.environ['BOT_TOKEN'])
