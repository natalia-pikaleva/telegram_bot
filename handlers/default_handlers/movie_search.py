from telebot.types import Message

from database.common.models import db, History
from settings import bot

from database.core import crud
from site_API.core import site_api, url, headers

import json

from datetime import datetime

from states.models import users_state, add_user, get_state


@bot.message_handler(commands=["movie_search"])
def bot_find_movie(message: Message):
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_movie_name()
    bot.reply_to(message, "Введите название фильма")


#  count = int(message.text)
#
#             with open("data.json", "r", encoding="utf-8") as data_file:
#                 data = json.load(data_file)
#
#             db_write = crud.create()
#
#             db_write(db, History, data)
#
#             for index_movie in range(min(len(data), count)):
#                 bot.reply_to(
#                     message, 'Информация о фильме "{}":'.format(index_movie + 1)
#                 )
#
#                 bot.reply_to(
#                     message, "Название: {}".format(data[index_movie]["message"]["name"])
#                 )
#                 bot.reply_to(
#                     message,
#                     "Описание: {}".format(data[index_movie]["message"]["description"]),
#                 )
#                 bot.reply_to(
#                     message,
#                     "Рейтинг: {}".format(data[index_movie]["message"]["rating"]),
#                 )
#                 bot.reply_to(
#                     message, "Год: {}".format(data[index_movie]["message"]["year"])
#                 )
#
#                 genres = ", ".join(
#                     [
#                         i_genre["name"]
#                         for i_genre in data[index_movie]["message"]["genres"]
#                     ]
#                 )
#
#                 bot.reply_to(message, "Жанр: {}".format(genres))
#                 bot.reply_to(
#                     message,
#                     "Возрастной рейтинг: {}".format(
#                         data[index_movie]["message"]["ageRating"]
#                     ),
#                 )
#                 bot.reply_to(
#                     message, "Постер: {}".format(data[index_movie]["message"]["poster"])
#                 )
#
#             user_data.clear()
#             count = 0
#
#         except Exception:
#             bot.reply_to(message, "Количество вариантов для вывода должно быть числом")
#             bot.reply_to(message, "Введите количество вариантов для вывода")
#

if __name__ == "__main__":
    bot_find_movie()
    search_movies()
    handle_text()
