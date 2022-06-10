import sys
import logging
import vk_api

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from logging import info as info_log, error as err_log, debug as dbg_log
import config_access
import steam_module
import steamid_module
import vk_module
from config_access import debug


version = 5.131

vk_session_group = vk_api.VkApi(token=config_access.access_token_group)
vk_group = vk_session_group.get_api()
longpoll = VkBotLongPoll(vk_session_group, config_access.group_id)


def start_app():
    for event in longpoll.listen():
        user_id = event.message["from_id"]
        text_message = event.message["text"]
        first_word = text_message.split(" ")[0].lower()
        if (first_word == "deep" or first_word == "fast") and len(text_message.split(" ")) == 2:
            vk_group.messages.send(user_id=user_id,
                                   message="Вы запустили {} поиск. Это может занять длительное время. Ожидайте... ".format(
                                       first_word),
                                   random_id=get_random_id())
            if first_word == "fast":
                result, count_steam_friend = steam_module.steam_friends_parser(text_message.split(" ")[-1])
            elif first_word == "deep":
                friends, nicknames, urls = steamid_module.get_full_info(steamid_module.get_steamid_page(text_message.split(" ")[-1]))
                result, count_steam_friend = friends

            else:
                err_log("Критическая ошибка в выборе режима, выход")
                sys.exit(0)

            vk_group.messages.send(user_id=user_id,
                                   message="Начинаем сканировать Steam. Анализ {} успешно найденых друзей. Подождите...".format(
                                       count_steam_friend),
                                   random_id=get_random_id())

            if text_message.split(" ")[1].split("/")[-1] == '':

                steam_id = text_message.split(" ")[1].split("/")[-2]
            else:
                steam_id = text_message.split(" ")[1].split("/")[-1]
            if debug:
                dbg_log(steam_id)
            if steam_id.isdigit():
                vk_group.messages.send(user_id=user_id,
                                       message="Steam id состоит только из цифр, анализировать не получится.",
                                       random_id=get_random_id())
            else:
                person = vk_module.valid_vk_friends([steam_id])
                if person:
                    vk_group.messages.send(user_id=user_id,
                                           message="Возможно наша цель найдена! *{}".format(steam_id),
                                           random_id=get_random_id())
                else:
                    vk_group.messages.send(user_id=user_id,
                                           message="К сожалению по айди найти не получилось...",
                                           random_id=get_random_id())

            final_text = vk_module.mutual_friends(result)
            statistics_message = "\nСтатистика по найденым общим друзьям: \n"
            if len(final_text[0]) == 0:
                final_text_friend = "Друзья из стима не найдены."
            else:
                final_text_friend = "\n".join(final_text[0])

            if len(final_text[1]) == 0:
                final_text_mutual = "Общие друзья у друзей не найдены."
            else:

                final_text_mutual = "\n".join(final_text[1])
                for count in final_text[2].keys():
                    statistics_message += "@id{} - {}, ".format(count, final_text[2].get(count))
            if debug:
                dbg_log(statistics_message)

            vk_group.messages.send(user_id=user_id,
                                   message=final_text_friend,
                                   random_id=get_random_id())
            vk_group.messages.send(user_id=user_id,
                                   message=final_text_mutual + "\n" + statistics_message,
                                   random_id=get_random_id())


if __name__ == '__main__':
    level = logging.INFO

    logging.basicConfig(
        format="\x1b[32m [%(asctime)s] |  [%(filename)s:%(lineno)d] | [%(levelname)s] | [%(message)s]",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
        handlers=[
            logging.FileHandler(config_access.file_log),
            logging.StreamHandler()
        ]
    )
    info_log("Program has been started!")
    info_log(f"Debug mode: {debug}")
    start_app()
