import discord
from discord.ext import commands

import json

from helpers.jsonreader import get_critter, get_monthly_critters
from helpers.serversettings import load_serversettings

class Critterpedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def fish(self, ctx, name:str, hemisphere:str=None):
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
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere)
        
        e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
        e.add_field(
            name=f'{critter_type.capitalize()} that have stayed since {critters["prev_month"]}', 
            value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
            inline=False
        )

        e.add_field(
            name=f'{critter_type.capitalize()} that are new for {critters["this_month"]}!',
            value=", ".join([critter['name'] for critter in critters['new_critters']]),
            inline=False
        )

        e.add_field(
            name=f'{critter_type.capitalize()} that will be leaving in {critters["next_month"]}',
            value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
            inline=False
        )

        await ctx.send(embed=e)
    

    @commands.command()
    async def nextmonth(self, ctx, critter_type:str, hemisphere:str=None):
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere, 0)
        
        e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
        e.add_field(
            name=f'{critter_type.capitalize()} that will stay after {critters["prev_month"]}', 
            value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
            inline=False
        )

        e.add_field(
            name=f'{critter_type.capitalize()} that will be new for {critters["this_month"]}!',
            value=", ".join([critter['name'] for critter in critters['new_critters']]),
            inline=False
        )
        
        e.add_field(
            name=f'{critter_type.capitalize()} that will be leaving in {critters["next_month"]}',
            value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
            inline=False
        )

        await ctx.send(embed=e)
    

    @commands.command()
    async def prevmonth(self, ctx, critter_type:str, hemisphere:str=None):
        if hemisphere is None:
            hemisphere = Critterpedia.__get_default_hemisphere(ctx)
        critters = get_monthly_critters(critter_type, hemisphere, -2)
        
        e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
        e.add_field(
            name=f'{critter_type.capitalize()} that were active since {critters["prev_month"]}', 
            value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
            inline=False
        )

        e.add_field(
            name=f'{critter_type.capitalize()} that were new to {critters["this_month"]}!',
            value=", ".join([critter['name'] for critter in critters['new_critters']]),
            inline=False
        )
        
        e.add_field(
            name=f'{critter_type.capitalize()} that left in {critters["next_month"]}',
            value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
            inline=False
        )
        
        await ctx.send(embed=e)


    def __critter_error():
        return "I am sorry, I could not find the critter you are looking for. Did you spell its name correctly?"
    

    def __get_default_hemisphere(ctx):
        serversettings = load_serversettings()
        
        guild_id = str(ctx.guild.id)
        if guild_id not in serversettings or serversettings[guild_id]['hemisphere'] is None:
            return 'northern'
        return serversettings[guild_id]['hemisphere']


def setup(bot):
    bot.add_cog(Critterpedia(bot))