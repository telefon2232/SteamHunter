import vk_api
import steam_module
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll


access_token_group = ""
access_token_user = ""
version = 5.131

vk_session_group = vk_api.VkApi(token=access_token_group)
vk_group = vk_session_group.get_api()
longpoll = VkBotLongPoll(vk_session_group, '209889779')

vk_session_user = vk_api.VkApi(token=access_token_user)
vk_user = vk_session_user.get_api()


def mutual_friends(array_friends):

    ids_user = []
    number_id = []
    message_friends = []
    mutual_finish = []

    for friend in array_friends:
        try:
            ids_user.append(vk_group.users.get(user_ids=friend, fields="city,domain"))

        except:
            continue

    for info in ids_user:
        info=info[0]
        user_id = info.get('id')
        domain = info.get('domain')
        city = info.get('city')
        number_id.append(user_id)
        if city is not None:
            city = city['title']
        else:
            city = "город не найден"
        message_friends.append("id{} ({})  - {}".format(user_id, domain, city))
        print("id{} ({})  - {}".format(user_id, domain, city))

    for i in range(len(number_id)):
        for j in range(i, len(number_id)+1):
           try:
                mutual = vk_user.friends.getMutual(source_uid=str(number_id[i]), target_uid=str(number_id[j]))
                if len(mutual) != 0:
                    mutual_finish.append("id{} и id{} имеют общих друзей: id{}".format(number_id[i], number_id[j], " id".join(list(map(str, mutual)))))
                    print("id{} и id{} имеют общих друзей: id{}".format(number_id[i], number_id[j], " id".join(list(map(str, mutual)))))
           except:
                continue
    return message_friends, mutual_finish


for event in longpoll.listen():
    user_id = event.message["from_id"]
    text_message = event.message["text"]
    if text_message.split(" ")[0].lower() == "чек" :
        vk_group.messages.send(user_id=user_id, message="Начинаем сканировать Steam",
                               random_id=get_random_id())
        steam_id = text_message.split(" ")[1].split("/")[-1]
        if steam_id.isdigit():
            vk_group.messages.send(user_id=user_id, message="Steam Id состоит только из цифр, анализировать не получится.",
                                   random_id=get_random_id())
        final_text = mutual_friends(steam_module.steam_friends_parser(text_message.split(" ")[-1]))
        if len(final_text[0]) == 0:
            final_text_friend = "Друзья из стима не найдены"
        else:
            final_text_friend = "\n".join(final_text[0])

        if len(final_text[1]) == 0:
            final_text_mutual = "Общие друзья у друзей не найдены"
        else:
            final_text_mutual = "\n".join(final_text[1])
        vk_group.messages.send(user_id=user_id, message=final_text_friend+"\n\n"+final_text_mutual, random_id=get_random_id())
