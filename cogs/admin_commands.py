import discord
from discord.ext import commands

import json

from helpers.checks import is_admin, is_owner, get_admins

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.check(is_admin)
    async def addadmin(self, ctx, member:discord.Member):
        adminlist = get_admins()
        if member.id in adminlist:
            await ctx.send(f'{member} is already an admin.')
        else:
            adminlist.append(member.id)
            self.__update_admin_list(adminlist)
            await ctx.send(f'{member} is now an admin!')

    @addadmin.error
    async def addadmin_error(self, ctx, error):
        await ctx.send(Admin.__admin_error())


    @commands.command()
    @commands.check(is_admin)
    async def removeadmin(self, ctx, member:discord.Member):
        adminlist = get_admins()
        if member.id not in adminlist:
            await ctx.send(f'{member} was never an admin to begin with!')
        else:
            adminlist.remove(member.id)
            self.__update_admin_list(adminlist)
            await ctx.send(f'{member} is no longer an administrator.')

    @removeadmin.error
    async def removeadmin_error(self, ctx, error):
        await ctx.send(Admin.__admin_error())


    def __admin_error(self):
        return "I'm afraid you don't have the necessary permissions to run that command hoo.."
    
    
    def __update_admin_list(self, adminlist):
        admins = {'admins': adminlist}
        with open('adminlist.json', 'w') as f:
            json.dump(admins, f)


def setup(client):
    client.add_cog(Admin(client))