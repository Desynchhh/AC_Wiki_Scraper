import discord
from discord.ext import commands

from helpers.jsonreader import get_critter

class Critterpedia(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command()
    async def fish(self, ctx, name:str, hemisphere:str='northern'):
        fish = get_critter('fish', name)
        if fish is None:
            await ctx.send(Critterpedia.__critter_error())
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


    @commands.command()
    async def bug(self, ctx, name:str, hemisphere:str='northern'):
        bug = get_critter('bugs', name)
        if bug is None:
            await ctx.send(Critterpedia.__critter_error())
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


    def __critter_error():
        return "I am sorry, I could not find the critter you are looking for. Did you spell its name correctly?"


def setup(client):
    client.add_cog(Critterpedia(client))