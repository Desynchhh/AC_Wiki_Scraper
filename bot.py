import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

from jsonreader import get_critter

load_dotenv()

# client = discord.Client()
client = commands.Bot(command_prefix='>')

@client.event
async def on_ready():
    print('Blathers, ready for action!')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

@client.command()
async def fish(ctx, name, hemisphere='northern'):
    fish = get_critter('fish', name)
    if fish is None:
        await ctx.send(could_not_find_critter_message())
        return
    message = f"""
{name.capitalize()}
Selling price: {fish['nook_price']}
C.J. selling price: {fish['cj_price']}
Location: {fish['location']}
Shadow size: {fish['shadow_size']}
Active hours: {fish['active_hours']}
Available in: {'All year' if len(fish['months_available'][hemisphere]) == 12 else ', '.join(fish['months_available'][hemisphere])}
More details at {fish['details_link']}"""
    await ctx.send(message)


@client.command()
async def bug(ctx, name, hemisphere='northern'):
    bug = get_critter('bugs', name)
    if bug is None:
        await ctx.send(could_not_find_critter_message())
        return
    message = f"""
{name.capitalize()}
Selling price: {bug['nook_price']}
Flick selling price: {bug['flick_price']}
Location: {bug['location']}
Active hours: {bug['active_hours']}
Available in: {'All year' if len(bug['months_available'][hemisphere]) == 12 else ', '.join(bug['months_available'][hemisphere])}
More details at {bug['details_link']}"""
    await ctx.send(message)


def could_not_find_critter_message():
    return "I am sorry, I could not find the critter you are looking for. Did you spell its name correctly?"

client.run(os.environ['BOT_TOKEN'])