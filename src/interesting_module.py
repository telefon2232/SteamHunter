import config_access
import vk_api
games_dict = {'dota': ['dota', 'дота', 'VK Dota 2', 'дота 2'],
     'cs': ['cs', 'кс', 'counter', "CS:GO HS"]
}

vk_session_user = vk_api.VkApi(token=config_access.access_token_user)
vk_user = vk_session_user.get_api()


def groups_analyzer(user_id):
    groups_list = vk_user.groups.get(user_id=user_id, extended=1).get("items")
    for i in groups_list:
        for j in games_dict.keys():
            if i.get("name") in games_dict.get(j):
                return i.get("name")
    return "Группы по играм не найдены."



#print(groups_analyzer(137516299))