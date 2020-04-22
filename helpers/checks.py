import discord

import json

def is_owner(ctx):
    return ctx.author.id == 228179496807694336


def is_admin(ctx):
    if is_owner(ctx):
        return True
    return ctx.author.id in get_admins()


def get_admins():
    with open('adminlist.json') as f:
        adminlist = json.load(f)
    return adminlist['admins']