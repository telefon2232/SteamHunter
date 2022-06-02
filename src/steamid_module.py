import time
import configparser
import json
import requests
import os
from bs4 import BeautifulSoup
from logging import info as info_log


main_dir = "\\".join(os.path.dirname(os.path.realpath(__file__)).split('\\')[:-1])
config = configparser.ConfigParser()

config.read(main_dir + "\\config.ini")

api_key = config["steamid"]["api_key"]
steam_id = config["steamid"]["steam_id"]
cookies = {'enwiki_session': config["custom"]["cookies"]}
useragent = config["custom"]["useragent"]
headers = {
    'User-Agent': useragent
}


def get_friends(link):
    id_friends = []

    service = "https://steamid.uk/profile/"
    if link[-1] == "/":
        link = link[:-1]
    if len(link.split("/")) == 1:
        steam_id = link
    else:
        steam_id = link.split("/")[-1]
    #print(steam_id)

    link_service = service + steam_id
    parser_service = requests.get(link_service, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(parser_service, 'html.parser')
    #print(soup)
    link_friends = str(soup.find_all("td", {"class": "d-md-table-cell"}))
   # print(link_friends)
    soup_friends = BeautifulSoup(link_friends, 'html.parser')
    link_friends = soup_friends.find_all("a")

    for i in link_friends:
        if "profile" in i['href']:
            id_friends.append(i['href'].split("/")[-1])

    get_url_json = []
    simple_step = []
    array_friends = "https://steamidapi.uk/v2/convert.php?myid=76561198267134991&apikey={}&input=".format(api_key)
    step_part = 100
    if len(id_friends) > step_part:
        for i in range(0, len(id_friends), step_part):
            simple_step.append(i)
        simple_step.append(len(id_friends) % step_part + simple_step[-1])
    else:
        simple_step = [0, len(id_friends)]
#    print(simple_step)
    if len(simple_step) > 2:
        for i in range(0, len(simple_step)-1):
            part_link = (array_friends + ",".join(id_friends[simple_step[i]:simple_step[i+1]]))
            temp_json = json.loads(requests.get(part_link).text).get("converted")
            for j in temp_json:
                get_url_json.append(j.get("inviteurl"))
    else:
            part_link = array_friends + ",".join(id_friends)
         #  print(part_link)
            temp_json = json.loads(requests.get(part_link).text).get("converted")
            for j in temp_json:
                get_url_json.append(j.get("inviteurl"))

    name_url_friends = []
    for i in get_url_json:
        time.sleep(0.1)
        name_url_friends.append(requests.get(str(i)).url)


   #print(name_url_friends)
    final_name_url_friends = []
    for i in name_url_friends:
        if not i.split("/")[-1].isdigit():
            final_name_url_friends.append(i.split("/")[-1])
    #print(final_name_url_friends)
    return final_name_url_friends, len(final_name_url_friends)


def get_nicknames():
    pass

def get_urls(link):
    service = "https://steamid.uk/profile/"
    if link[-1] == "/":
        link = link[:-1]
    if len(link.split("/")) == 1:
        steam_id = link
    else:
        steam_id = link.split("/")[-1]
    # print(steam_id)

    link_service = service + steam_id
    parser_service = requests.get(link_service, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(parser_service, 'html.parser')
    #print(soup)
    link_friends = soup.find_all("span", {"class": "label label-default"})
    old_urls = []
    for i in link_friends:
        if i.a:
            old_urls.append(i.a.text)
    info_log(old_urls)
    return old_urls
  #  print(link_friends)

#get_urls("https://steamid.uk/profile/76561198023414915")
#get_friends("https://steamcommunity.com/id/thredriper3990x")
