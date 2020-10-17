import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import os

from helpers.serversettings import Serversettings
from scraper_v2 import run_scraper
from logger import log_error


# Load .env file
load_dotenv()

# Load custom server settings
def get_prefix(bot:discord.ext.commands.Bot, message:discord.ext.commands.Context) -> str:
    """Gets the prefix for the server. Returns the global default if one is not set.

    :type bot: discord.ext.commands.Bot
    :type message: discord.ext.commands.Context
    :rtype: str
    """
    if not message.guild:
        return commands.when_mentioned_or(os.environ['BOT_PREFIX'])(bot, message)
    
    serversettings = Serversettings().load()

    guild_id = str(message.guild.id)    
    if guild_id not in serversettings or 'prefix' not in serversettings[guild_id]:
        return commands.when_mentioned_or(os.environ['BOT_PREFIX'])(bot, message)

    prefix = serversettings[guild_id]['prefix']
    return commands.when_mentioned_or(prefix)(bot, message)


# Bot settings
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=228179496807694336)
bot.remove_command('help')

@bot.event
async def on_ready():
    """The bot's on_ready event. Starts background tasks as well as notifies the console the bot is ready."""
    # update_critterpedia.start()
    print('Celeste, ready for action!')


@bot.event
async def on_command_error(ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
    """Handles errors that are not specific to cogs. Sends out an informing message to the relevant discord channel.

    :type ctx: discord.ext.commands.Context
    :type error: discord.ext.commands.errors.DiscordException
    :raises error: Raises the error if the generic handler was unable to handle it, so other handlers can take care of it.
    """
    await log_error(ctx, error)
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("I'm afraid that command does not exist")
    elif isinstance(error, discord.ext.commands.errors.TooManyArguments):
        await ctx.send("Calm down there! You're giving me WAY too many arguments for that command!")
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError) and isinstance(error.original, discord.errors.Forbidden):
        await ctx.send("I'm afraid I don't have the required permissions to do that")
    else:
        raise error


# @tasks.loop(hours=168)
# async def update_critterpedia():
#     """Background task that runs the wiki scraper once a week, just in case anything changes once in a while."""
#     await run_scraper()


# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Run bot
if __name__ == '__main__':
    bot.run(os.environ['BOT_TOKEN'])
