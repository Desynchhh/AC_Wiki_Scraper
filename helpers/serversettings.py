import json

SERVERSETTINGS_PATH = 'serversettings.json'

def load_serversettings():
    with open(SERVERSETTINGS_PATH, 'r') as f:
        return json.load(f)


def update_serversettings(serversettings:dict):
    with open(SERVERSETTINGS_PATH, 'w') as f:
        json.dump(serversettings, f)


def get_prefix(ctx):
    serversettings = load_serversettings()
    guild_id = str(ctx.guild.id)
    if guild_id in serversettings and 'prefix' in serversettings[guild_id]:
        return serversettings[guild_id]['prefix']
    else:
        return '>'


def get_hemisphere(ctx):
    serversettings = load_serversettings()
    guild_id = str(ctx.guild.id)
    if guild_id in serversettings and 'hemisphere' in serversettings[guild_id]:
        return serversettings[guild_id]['hemisphere']
    else:
        return 'northern'