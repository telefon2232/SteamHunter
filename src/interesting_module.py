import vk_module

games_list = [
    {
        'id': 'dota',
        'value': ['dota', 'дота', 'dota2', 'дота2']
    },
    {
        'id': 'cs',
        'value': ['cs', 'кс', 'counter']
    }
]


def groups_analyzer(user_id_check, send_id):
    groups_list = user_session.method('groups.get', {'user_id': user_id_check, 'extended': 1}).get('items')
    game_counter = {}
    for i in range(len(groups_list)):
        for theme in games_list:
            for item in theme.get('value'):
                if " " + item + " " in (" " + groups_list[i]['name'].lower() + " "):
                    if theme.get('id') in game_counter.keys():
                        game_counter[theme.get('id')] = game_counter.get(theme.get('id')) + 1
                    else:
                        game_counter[theme.get('id')] = 1
    return game_counter
