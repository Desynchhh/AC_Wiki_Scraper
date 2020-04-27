import discord
from discord.ext import commands

import json

from helpers.jsonreader import get_critter, get_monthly_critters

class Critterpedia(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command()
    async def fish(self, ctx, name:str, hemisphere:str=None):
        """Show info on a specific fish.
        <name>: name of the fish.
        OPTIONAL: <hemisphere> is northern by default, but can be set to southern.
        Example: >fish bitterling southern"""        
        fish = get_critter('fish', name, hemisphere)
        if fish is None:
            await ctx.send(Critterpedia.__critter_error())
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)

        message = f"""
{fish['name']}
Selling price: {fish['nook_price']}
C.J. selling price: {fish['cj_price']}
Location: {fish['location']}
Shadow size: {fish['shadow_size']}
Active hours: {fish['active_hours']}
Available in ({hemisphere}): {'All year' if len(fish['months_available'][hemisphere]) == 12 else ', '.join(fish['months_available'][hemisphere])}
More details at {fish['details_link']}"""
        await ctx.send(message)


    @commands.command()
    async def bug(self, ctx, name:str, hemisphere:str=None):
        """Show info on a specific bug.
        <name>: Name of the bug.
        OPTIONAL: <hemisphere>: Northern by default, but can be set to southern.
        Example: >bug wasp southern"""
        bug = get_critter('bugs', name, hemisphere)
        if bug is None:
            await ctx.send(Critterpedia.__critter_error())
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)

        message = f"""
{bug['name']}
Selling price: {bug['nook_price']}
Flick selling price: {bug['flick_price']}
Location: {bug['location']}
Active hours: {bug['active_hours']}
Available in ({hemisphere}): {'All year' if len(bug['months_available'][hemisphere]) == 12 else ', '.join(bug['months_available'][hemisphere])}
More details at {bug['details_link']}"""
        await ctx.send(message)
    

    @commands.command()
    async def thismonth(self, ctx, critter_type:str, hemisphere:str=None):
        """Shows all available fish or bugs for this month.
        <critter_type>: Set to either fish or bugs, depending what you want to know more about.
        OPTIONAL: <hemisphere>: Northern by default, but can be set to southern.
        Example: >thismonth fish"""
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere)
        message = f'The {critter_type} you can catch this month are the {", ".join(critters)}'
        await ctx.send(message)
    

    @commands.command()
    async def nextmonth(self, ctx, critter_type:str, hemisphere:str=None):
        """Shows all available fish or bugs for next month.
        <critter_type>: Set to either fish or bugs, depending what you want to know more about.
        OPTIONAL: <hemisphere>: Northern by default, but can be set to southern.
        Example: >nextmonth fish"""
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere, 0)
        message = f'The {critter_type} you can catch next month are the {", ".join(critters)}'
        await ctx.send(message)
    

    @commands.command()
    async def prevmonth(self, ctx, critter_type:str, hemisphere:str=None):
        """Shows all fish or bugs that were available last month.
        <critter_type>: Set to either fish or bugs, depending what you want to know more about.
        OPTIONAL: <hemisphere>: Northern by default, but can be set to southern.
        Example: >prevmonth fish"""
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere, -2)
        message = f'The {critter_type} you could have caught last month were the {", ".join(critters)}'
        await ctx.send(message)


    def __critter_error():
        return "I am sorry, I could not find the critter you are looking for. Did you spell its name correctly?"
    

    def __get_default_hemisphere(ctx):
        with open('serversettings.json', 'r') as f:
            serversettings = json.load(f)
        
        guild_id = str(ctx.guild.id)
        if guild_id not in serversettings or serversettings[guild_id]['hemisphere'] is None:
            return 'northern'
        return serversettings[guild_id]['hemisphere']


def setup(client):
    client.add_cog(Critterpedia(client))