import json

#TODO: add list of valid keys, possibly valid value types ?enum
class ConfigHelper():
    def __init__(self):
        # self.get_all_configs() #TODO: maintain "self.conf" that stores copy of configs aka reduce context manager usage
        pass

    def get_config(self, key: str): # validation
        with open("config.json", "r") as f:
            return json.load(f)[key]
    
    def set_config(self, key: str, val): # validation
        with open("config.json", "w") as f:
            json.dump({key: val}, f)
            