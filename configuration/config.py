import configparser

config = configparser.ConfigParser()
config.read("settings.conf")

CONFIG = {}

for section in config.sections():
    for key in config[section]:
        CONFIG[key.upper()] = config[section][key]
