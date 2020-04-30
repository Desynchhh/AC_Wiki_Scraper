import json


class Serversettings():
    def __init__(self):
        self.SERVERSETTINGS_PATH = 'serversettings.json'


    def load(self):
        with open(self.SERVERSETTINGS_PATH, 'r') as f:
            return json.load(f)


    def update(self, serversettings:dict):
        with open(self.SERVERSETTINGS_PATH, 'w') as f:
            json.dump(serversettings, f)


    def get_prefix(self, guild_id):
        serversettings = self.load()
        guild_id = str(guild_id)
        if guild_id in serversettings and 'prefix' in serversettings[guild_id]:
            return serversettings[guild_id]['prefix']
        else:
            return '>'


    def get_hemisphere(self, guild_id):
        serversettings = self.load()
        guild_id = str(guild_id)
        if guild_id in serversettings and 'hemisphere' in serversettings[guild_id]:
            return serversettings[guild_id]['hemisphere']
        else:
            return 'northern'