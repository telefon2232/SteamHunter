
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

    for i in range(len(number_id)):
        for j in range(i, len(number_id)):
            try:
                mutual = vk_user.friends.getMutual(source_uid=str(number_id[i]), target_uid=str(number_id[j]))

                if len(mutual) != 0:
                    mutual_finish.append(
                        "✅ @id{} ({}) и @id{} ({}) имеют общих друзей: @id{}\n".format(number_id[i], domain_id[i],
                                                                                       number_id[j], domain_id[j],
                                                                                       " @id".join(
                                                                                           list(map(str, mutual)))))
                    array_mutual_friends += mutual

                    if debug:
                        dbg_log("id{} и id{} имеют общих друзей: id{}".format(number_id[i], number_id[j],
                                                                              " id".join(list(map(str, mutual)))))
            except Exception as e:
                err_log(f"Критическая ошибка в анализе общих друзей:\n {e}")
    for i in array_mutual_friends:
        dict_friends[i] = dict_friends.get(i, 0) + 1

    if debug:
        dbg_log(array_mutual_friends)
        dbg_log(dict_friends)
   # print(mutual_finish,dict_friends)
    return message_friends, mutual_finish, dict_friends


# print(mutual_friends([152385596,78157424]))