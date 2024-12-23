import ast
import json
from pprint import pprint

from telebot.types import Message
from settings import bot
from database.core import crud
from database.common.models import db, History
from states.models import users_state, add_user, get_state
from .start import db_read


def send_message(user_id, data):
    """
    Функция получает на входе id чата и список фильмов и выводит в чат информацию
    об этих фильмах
    :param user_id: id чата
    :param data: список фильмов
    """

    bot.send_message(user_id, "Название: {}".format(data["name"]))
    bot.send_message(
        user_id,
        "Описание: {}".format(data["description"]),
    )
    bot.send_message(
        user_id,
        "Рейтинг: {}".format(data["rating"]),
    )
    bot.send_message(user_id, "Год: {}".format(data["year"]))

    genres = ", ".join([i_genre["name"] for i_genre in data["genres"]])

    bot.send_message(user_id, "Жанр: {}".format(genres))
    bot.send_message(
        user_id,
        "Возрастной рейтинг: {}".format(data["ageRating"]),
    )
    bot.send_message(user_id, "Постер: {}".format(data["poster"]))


@bot.message_handler(commands=["history"])
def bot_history(message: Message):
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    bot.reply_to(message, "История запросов:")

    retrieved = db_read(db, History, History.date, History.movie_info)

    for element in retrieved:
        bot.send_message(user_id, "Дата: {}:".format(element.date))

        movies_list = ast.literal_eval(element.movie_info)

        for i_movie in movies_list:
            send_message(user_id, i_movie)


if __name__ == "__main__":
    bot_history()
