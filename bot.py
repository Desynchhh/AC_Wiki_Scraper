import discord
from discord.ext import commands
from dotenv import load_dotenv

import os, json

# Load .env file
load_dotenv()

# Load custom server settings
def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or('>')(bot, message)
    
    with open('serversettings.json', 'r') as f:
        serversettings = json.load(f)

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


# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Run bot
bot.run(os.environ['BOT_TOKEN'])