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
async def fish(ctx, fish_name, hemisphere='northern'):
    fish = get_critter('fish', fish_name)
    if fish is None:
        await ctx.send("I am sorry, I could not find the fish you are looking for. Did you spell it's name correctly?")
        return
    await ctx.send(f"""
{fish_name.capitalize()}
Selling price: {fish['nook_price']}
C.J. selling price: {fish['cj_price']}
Location: {fish['location']}
Shadow size: {fish['shadow_size']}
Active hours: {fish['active_hours']}
Available in: {', '.join(fish['months_available'][hemisphere])}
More details at {fish['details_link']}""")


client.run(os.environ['BOT_TOKEN'])