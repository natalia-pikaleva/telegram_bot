import ast

from telebot.types import Message
from settings import bot

from states.models import users_state, add_user, get_state

from database.common.models import History, db

from database.core import db_read


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
        "За какую дату вывести историю запросов? Введите дату в формате: dd.mm или dd.mm.yy",
    )


def send_message_history(user_id: int, data: dict) -> None:
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


def print_history(user_id: int, date: str) -> None:
    """
    Функция получает на входе id чата и дату и выводит в чат бота историю запросов на эту дату
    :param user_id: id чата
    :param date: дата, за которую нужно вывести историю запросов
    """

    bot.send_message(user_id, "История запросов за {}: ".format(date))

    retrieved = db_read(db, History, History.date, History.movie_info, History.user_id)

    flag = True
    for element in retrieved:
        history_user_id = int(element.user_id)
        history_date = element.date

        if history_user_id == user_id and history_date == date:
            flag = False

            movies_list = ast.literal_eval(element.movie_info)

            for i_movie in movies_list:
                send_message_history(user_id, i_movie)

    if flag:
        bot.send_message(user_id, "На указанную дату не было запросов")
