import time

import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from logging import info as info_log, error as err_log, debug as dbg_log
import config_access
from config_access import debug

vk_session_group = vk_api.VkApi(token=config_access.access_token_group)
vk_group = vk_session_group.get_api()
longpoll = VkBotLongPoll(vk_session_group, config_access.group_id)

vk_session_user = vk_api.VkApi(token=config_access.access_token_user)
vk_user = vk_session_user.get_api()


def valid_vk_friends(array_friends):
    ids_user = []
    for friend in array_friends:
        try:
            user = vk_group.users.get(user_ids=friend, fields="city,domain")
            if user:
                ids_user.append(user)
        except Exception as e:
            err_log(f"Критическая ошибка в анализе валидных друзей:\n {e}")
    return ids_user


def get_friends_user(array_friends,domain_id):


    friend_list = []
    mutual_finish = []
    array_mutual_friends = []

    for friend in array_friends:
        try:
            user = vk_user.friends.get(user_id=friend)
            if user:
                friend_list.append(user.get("items"))
        except Exception as e:
            err_log(f"Критическая ошибка в анализе валидных друзей:\n {e}")

    for i in range(len(array_friends)):
        for j in range(i+1,len(array_friends)):

            mutual = list(set(friend_list[i]) & set(friend_list[j]))
            if len(mutual) != 0:
                array_mutual_friends+=mutual
                mutual_finish.append("✅ @id{} ({}) и @id{} ({}) имеют общих друзей: @id{}\n".format(array_friends[i], domain_id[i],
                                                                                       array_friends[j], domain_id[j],
                                                                                       " @id".join(
                                                                                           list(map(str, mutual)))))


    if debug:
        dbg_log(mutual_finish)


    return mutual_finish,array_mutual_friends

#print(get_friends_user([137000677,137516299],["an","iv"]))


def mutual_friends(array_friends):
    number_id = []
    domain_id = []
    message_friends = []
    mutual_finish = []
    array_mutual_friends = []
    dict_friends = {}

    ids_user = valid_vk_friends(array_friends)
    for info in ids_user:
        if debug:
            pass
           # info_log(info)
        info = info[0]
        # print(info)
        user_id = info.get('id')
        domain = info.get('domain')
        city = info.get('city')
        if info.get("can_access_closed") and not info.get("deactivated"):
            number_id.append(user_id)
            domain_id.append(domain)

        if city is not None:
            city = city['title']
        else:
            city = "Город не найден"
        message_friends.append("@id{} ({})  - {}".format(user_id, domain, city))
        if debug:
            dbg_log("id{} ({})  - {}".format(user_id, domain, city))
    mutual_finish, array_mutual_friends = get_friends_user(number_id,domain_id)

    for i in array_mutual_friends:
        dict_friends[i] = dict_friends.get(i, 0) + 1

    if debug:
        dbg_log(array_mutual_friends)
        dbg_log(dict_friends)
   # print(mutual_finish,dict_friends)
    return message_friends, mutual_finish, dict_friends


# print(mutual_friends([152385596,78157424]))

def get_probability(targets):
    games_dict = {'dota': ['dota', 'дота', 'vk dota 2', 'дота 2'],
                  'cs': ['cs', 'кс', 'counter', "cs:go hs"]
                  }
    probability = {}
    sex = []  # Не было (Пол)
    interesting = []  # Анализ интересов
    last_connect = []  # Последний заход
    count_target = []  # Количество совпадений в общих
    word_in_status = []  # Слова в статусе
    count_of_friends = []  # Количество друзей (5000+ друзей скорее всего неправильный результат)
    name_of_videos = []  # Названия в видео могут быть связаны с игрой
    summary = vk_group.users.get(user_ids=targets, fields="domain,games,last_seen,online,sex,status")
    for target in summary:
        print(target)
        if target.get("sex") == 2:
            probability[target.get("id")] = 16

    print(target)



#get_probability([152385596])




















