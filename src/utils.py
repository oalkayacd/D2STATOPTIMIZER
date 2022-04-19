import json
from configparser import ConfigParser

def readJSON(filepath):
    with open(filepath, 'r') as f:
        wep_data = json.load(f)
    return wep_data    


def readConfig():
    config = ConfigParser()
    config.read('src/config.cfg')
    return config
