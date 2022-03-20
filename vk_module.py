import vk_api
import steam_module
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll

access_token_group = ""
access_token_user = ""
version = 5.131
debug = True
vk_session_group = vk_api.VkApi(token=access_token_group)
vk_group = vk_session_group.get_api()
longpoll = VkBotLongPoll(vk_session_group, '')

vk_session_user = vk_api.VkApi(token=access_token_user)
vk_user = vk_session_user.get_api()


def valid_vk_friends(array_friends):
    ids_user = []
    for friend in array_friends:
        try:
            user = vk_group.users.get(user_ids=friend, fields="city,domain")
            if user:
                ids_user.append(user)
        except:
            continue
    return ids_user


def mutual_friends(array_friends):
    number_id = []
    message_friends = []
    mutual_finish = []
    ids_user = valid_vk_friends(array_friends)

    for info in ids_user:
        if not info:
            continue
        if debug:
            print(info)
        info = info[0]
        # print(info)
        user_id = info.get('id')
        domain = info.get('domain')
        city = info.get('city')
        if not info.get("is_closed") and not info.get("deactivated"):
            number_id.append(user_id)
        if city is not None:
            city = city['title']
        else:
            city = "Город не найден"
        message_friends.append("@id{} [{}]  - {}".format(user_id, domain, city))
        if debug:
            print("id{} ({})  - {}".format(user_id, domain, city))

    for i in range(len(number_id)):
        for j in range(i, len(number_id)):
            try:
                mutual = vk_user.friends.getMutual(source_uid=str(number_id[i]), target_uid=str(number_id[j]))

                if len(mutual) != 0:
                    mutual_finish.append("@id{} и @id{} имеют общих друзей: @id{}".format(number_id[i], number_id[j],
                                                                                          " @id".join(
                                                                                              list(map(str, mutual)))))
                    if debug:
                        print("id{} и id{} имеют общих друзей: id{}".format(number_id[i], number_id[j],
                                                                            " id".join(list(map(str, mutual)))))
            except Exception as e:
                print("Критическая ошибка в анализе общих друзей:\n", e)
    return message_friends, mutual_finish


# print(mutual_friends([323516185,217025049]))

for event in longpoll.listen():
    user_id = event.message["from_id"]
    text_message = event.message["text"]
    if text_message.split(" ")[0].lower() == "чек" and len(text_message.split(" ")) == 2:
        result, count_steam_friend = steam_module.steam_friends_parser(text_message.split(" ")[-1])
        vk_group.messages.send(user_id=user_id,
                               message="Начинаем сканировать Steam. Анализ {} успешно найденых друзей. Подождите...".format(
                                   count_steam_friend),
                               random_id=get_random_id())

        if text_message.split(" ")[1].split("/")[-1] == '':

            steam_id = text_message.split(" ")[1].split("/")[-2]
        else:
            steam_id = text_message.split(" ")[1].split("/")[-1]
        if debug:
            print(steam_id)
        if steam_id.isdigit():
            vk_group.messages.send(user_id=user_id,
                                   message="Steam id состоит только из цифр, анализировать не получится.",
                                   random_id=get_random_id())
        else:
            person = valid_vk_friends([steam_id])
            if person:
                vk_group.messages.send(user_id=user_id,
                                       message="Возможно наша цель найдена! *{}".format(steam_id),
                                       random_id=get_random_id())
            else:
                vk_group.messages.send(user_id=user_id,
                                       message="К сожалению по айди найти не получилось...",
                                       random_id=get_random_id())

        final_text = mutual_friends(result)
        if len(final_text[0]) == 0:
            final_text_friend = "Друзья из стима не найдены."
        else:
            final_text_friend = "\n".join(final_text[0])

        if len(final_text[1]) == 0:
            final_text_mutual = "Общие друзья у друзей не найдены."
        else:
            final_text_mutual = "\n".join(final_text[1])
        vk_group.messages.send(user_id=user_id, message=final_text_friend + "\n\n" + final_text_mutual,
                               random_id=get_random_id())
