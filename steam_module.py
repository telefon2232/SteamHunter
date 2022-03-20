import requests
from bs4 import BeautifulSoup


def steam_friends_parser(link):
    friends_steam = link + "/friends"
    html_friend = requests.get(friends_steam).text

    soup = BeautifulSoup(html_friend, 'html.parser')
    selectable_overlay = soup.find_all("a", {"class": "selectable_overlay"})

    friends_link_array = []
    friends_valid_link = []
    for i in selectable_overlay:
        friends_link_array.append(i["href"].split("/")[-1])
    if len(friends_link_array) == 0:
        return []
    for i in friends_link_array:
        if not i.isdigit():
            friends_valid_link.append(i)

    return friends_valid_link, len(friends_valid_link)
