import vk_module

dota_names = ['dota', 'дота', 'cs', 'кс', 'counter']


def interesting(user_id_check, send_id):
    groups_list = vk_module.vk_session_user.method('groups.get', {'user_id': user_id_check, 'extended': 1}).get('items')
    print(groups_list)
    count_game_public = 0
    for i in range(len(groups_list)):
        for word in dota_names:
            if word in groups_list[i]['name'].lower():
                count_game_public = count_game_public + 1
    vk_module.vk_group.messages.send(send_id, 'Count Of Gamer Groups:' + str(count_game_public))
