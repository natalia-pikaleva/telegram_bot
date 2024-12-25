import ast
import json
from pprint import pprint
import flet

from telebot.types import Message
from settings import bot
from database.core import crud
from database.common.models import db, History
from states.models import users_state, add_user, get_state
from .start import db_read


def send_message(user_id: int, data: dict) -> None:
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


@bot.message_handler(func=lambda message: message.text == "Просмотр истории запросов")
def bot_history(message: Message) -> None:
    """
    Функция получает на входе команду history и переключает состояние
    пользователя на choosing_date_of_history
    :param message: сообщение пользователя
    """

    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_date_of_history()
    bot.reply_to(
        message,
        "За какую дату вывести историю запросов?",
    )


def print_history(user_id: int, date: str) -> None:
    """
    Функция получает на входе id чата и дату и выводит в чат бота историю запросов на эту дату
    :param user_id: id чата
    :param date: дата, за которую нужно вывести историю запросов
    """

    bot.send_message(user_id, "История запросов за {}:".format(date))

    retrieved = db_read(db, History, History.date, History.movie_info)

    flag = True
    for element in retrieved:
        history_date = element.date

        if history_date == date:
            flag = False

            movies_list = ast.literal_eval(element.movie_info)

            for i_movie in movies_list:
                send_message(user_id, i_movie)

    if flag:
        bot.send_message(user_id, "На указанную дату не было запросов")
