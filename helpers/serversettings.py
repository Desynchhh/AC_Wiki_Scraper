import json, os


class Serversettings():
    def __init__(self):
        self.SERVERSETTINGS_PATH = 'serversettings.json'


    def __check_file(self):
        """Ensures the serversettings JSON file exists."""
        if not os.path.exists(self.SERVERSETTINGS_PATH) and not os.path.isfile(self.SERVERSETTINGS_PATH):
            default_contents = {
                "valid_hemispheres": {
                    "northern": ["northern", "north", "nor", "n"],
                    "southern": ["southern", "south", "sou", "s"]
                },
                "servers": {}
            }
            with open(self.SERVERSETTINGS_PATH, 'w') as f:
                json.dump(default_contents, f)


    def load(self) -> dict:
        """Returns all server data in the serversettings JSON file.

        :rtype: dict
        """
        self.__check_file()
        with open(self.SERVERSETTINGS_PATH, 'r') as f:
            return json.load(f)['servers']


    def update(self, serversettings:dict):
        """Updates server configuration in the serversettings JSON file.

        :type serversettings: dict
        """
        self.__check_file()
        with open(self.SERVERSETTINGS_PATH, 'r') as f:
            s = json.load(f)
        s['servers'] = serversettings
        with open(self.SERVERSETTINGS_PATH, 'w') as f:
            json.dump(s, f)


    def get_prefix(self, guild_id) -> str:
        """Returns the prefix of the given server id.

        :type guild_id: int
        :rtype: str
        """
        self.__check_file()
        serversettings = self.load()
        guild_id = str(guild_id)
        if guild_id in serversettings and 'prefix' in serversettings[guild_id]:
            return serversettings[guild_id]['prefix']
        else:
            return os.environ['BOT_PREFIX']
    

    def get_valid_hemispheres(self) -> str:
        """Returns the valid hemisphere data in the serversettings JSON file.

        :rtype: str
        """
        self.__check_file()
        with open(self.SERVERSETTINGS_PATH, 'r') as f:
            return json.load(f)['valid_hemispheres']


    def get_hemisphere(self, guild_id) -> str:
        """Returns the given server's default hemisphere. Northern if none is set.

        :type guild_id: int
        :rtype: str
        """
        self.__check_file()
        serversettings = self.load()
        guild_id = str(guild_id)
        if guild_id in serversettings and 'hemisphere' in serversettings[guild_id]:
            return serversettings[guild_id]['hemisphere']
        else:
            return 'northern'