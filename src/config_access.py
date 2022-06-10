import os
import configparser


main_dir = "\\".join(os.path.dirname(os.path.realpath(__file__)).split('\\')[:-1])
config = configparser.ConfigParser()

config.read(main_dir + "\\config.ini")

access_token_group = config["vk"]["access_token_group"]
access_token_user = config["vk"]["access_token_user"]
group_id = config["vk"]["group_id"]
file_log = config["custom"]["log_filename"]

api_key = config["steamid"]["api_key"]
myid = config["steamid"]["steam_id"]

cookies = {'enwiki_session': config["custom"]["cookies"]}
useragent = config["custom"]["useragent"]
headers = {
    'User-Agent': useragent
}

debug = True  # Temp var, need to move to config

