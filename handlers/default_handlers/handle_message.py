from datetime import datetime
from dateutil import parser

from telebot.types import Message

from database.common.models import History, db

from settings import bot

from states.models import users_state, add_user, get_state
from .start import db_write
from .movie_by_rating import search_movies_with_rating
from .movie_search import search_movies
from .low_budget_movie import search_movies_low_budget
from .high_budget_movie import search_movies_high_budget
from .history import print_history


def send_message(user_id, data):
    """
    Функция получает на входе id чата и список фильмов и выводит в чат информацию
    об этих фильмах
    :param user_id: id чата
    :param data: список фильмов
    """

    if len(data) == 0:
        bot.send_message(user_id, "По вашему запросу фильмы не найдены")

    for index_movie in range(len(data)):
        bot.send_message(user_id, 'Информация о фильме "{}":'.format(index_movie + 1))

        bot.send_message(user_id, "Название: {}".format(data[index_movie]["name"]))

        try:
            bot.send_message(
                user_id,
                "Бюджет фильма: {}".format(data[index_movie]["budget"]["value"]),
            )
        except Exception:
            print()

        bot.send_message(
            user_id,
            "Описание: {}".format(data[index_movie]["description"]),
        )
        bot.send_message(
            user_id,
            "Рейтинг: {}".format(data[index_movie]["rating"]),
        )
        bot.send_message(user_id, "Год: {}".format(data[index_movie]["year"]))

        genres = ", ".join([i_genre["name"] for i_genre in data[index_movie]["genres"]])

        bot.send_message(user_id, "Жанр: {}".format(genres))
        bot.send_message(
            user_id,
            "Возрастной рейтинг: {}".format(data[index_movie]["ageRating"]),
        )
        bot.send_message(user_id, "Постер: {}".format(data[index_movie]["poster"]))

    data_history = {"date": datetime.now().strftime("%Y-%m-%d"), "movie_info": data}

    db_write(db, History, data_history)


@bot.message_handler(content_types=["text"])
def handle_message(message: Message, info_for_find={}) -> None:
    """
    Функция получает на входе сообщение пользователя и обрабатывает его в зависимости
    от состояния пользователя на данный момент
    :param message: сообщение пользователя
    :param info_for_find: словарь с информацией для поисковых запросов
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    state = get_state(user_id)

    if state == "choosing_movie_name":
        # Команда Найти информацию о фильме, этап Ввод названия фильма
        movie_name = message.text.capitalize()
        info_for_find["movie_name"] = movie_name
        bot.reply_to(message, "Введите жанр фильма")
        users_state[user_id].machine.choose_movie_genre()

    elif state == "choosing_movie_genre":
        # Команда Найти информацию о фильме, этап Ввод жанра
        movie_genre = message.text.lower()
        info_for_find["movie_genre"] = movie_genre
        bot.reply_to(message, "Введите количество фильмов для вывода")
        users_state[user_id].machine.choose_count_movies()

    elif state == "choosing_count_movies":
        # Команда Найти информацию о фильме, этап Ввод количество фильмов к выводу
        try:
            count_movies = int(message.text)
            info_for_find["count_movies"] = count_movies

            data = search_movies(
                movie_name=info_for_find["movie_name"],
                genre=info_for_find["movie_genre"],
                count_movies=info_for_find["count_movies"],
            )

            send_message(user_id, data)
            users_state[user_id].machine.final()

        except Exception as ex:
            print(ex)

            bot.reply_to(message, "Количество фильмов должно быть числом")
            bot.reply_to(message, "Введите количество фильмов для получения информации")

    elif state == "choosing_movie_rating":
        # Команда Найти фильм по рейтингу, этап Ввод рейтинга

        try:
            movie_rating = float(message.text.replace(",", "."))
            info_for_find["movie_rating"] = movie_rating

            bot.reply_to(message, "Введите количество фильмов для вывода")
            users_state[user_id].machine.choose_count_movie_rating()

        except Exception as ex:
            print(ex)

            bot.reply_to(message, "Рейтинг должен быть числом, например 8.5 или 9")
            bot.reply_to(message, "Введите рейтинг")

    elif state == "choosing_count_movie_rating":
        # Команда Найти фильм по рейтингу, этап Ввод количества фильмов к выводу

        try:
            count_movies = int(message.text)
            data = search_movies_with_rating(
                info_for_find["movie_rating"], count_movies
            )
            send_message(user_id, data)

            users_state[user_id].machine.final()

        except Exception as ex:
            print(ex)

            bot.reply_to(message, "Количество фильмов должно быть числом")
            bot.reply_to(message, "Введите количество фильмов для получения информации")

    elif state == "choosing_low_budget_movie":
        # Команда Найти фильм с низким бюджетом, этап Ввод суммы бюджета

        try:
            info_for_find["budget"] = int(message.text)

            bot.reply_to(message, "Введите количество фильмов для вывода")

            users_state[user_id].machine.choose_count_low_budget()

        except Exception as ex:
            print(ex)

            bot.reply_to(
                message, "Бюджет фильма должен быть целым числом, например 250 000"
            )
            bot.reply_to(message, "Введите сумму бюджета для поиска фильмов")

    elif state == "choosing_count_low_budget_movie":
        # Команда Найти фильм с низким бюджетом, этап Ввод количества фильмов к выводу

        try:
            count_movies = int(message.text)

            data = search_movies_low_budget(info_for_find["budget"], count_movies)

            send_message(user_id, data)
            users_state[user_id].machine.final()

        except Exception as ex:
            print(ex)

            bot.reply_to(message, "Количество фильмов должно быть числом")
            bot.reply_to(message, "Введите количество фильмов для получения информации")

    elif state == "choosing_high_budget_movie":
        # Команда Найти фильм с высоким бюджетом, этап Ввод суммы бюджета

        try:
            info_for_find["budget"] = int(message.text)

            bot.reply_to(message, "Введите количество фильмов для вывода")

            users_state[user_id].machine.choose_count_high_budget()

        except Exception as ex:
            print(ex)

            bot.reply_to(
                message, "Бюджет фильма должен быть целым числом, например 250 000"
            )
            bot.reply_to(message, "Введите сумму бюджета для поиска фильмов")

    elif state == "choosing_count_high_budget_movie":
        # Команда Найти фильм с высоким бюджетом, этап Ввод количества фильмов к выводу

        try:
            count_movies = int(message.text)

            data = search_movies_high_budget(info_for_find["budget"], count_movies)

            send_message(user_id, data)
            users_state[user_id].machine.final()

        except Exception as ex:
            print(ex)

            bot.reply_to(message, "Количество фильмов должно быть числом")
            bot.reply_to(message, "Введите количество фильмов для получения информации")

    elif state == "start":
        # Состояние Старт - пользователь отправил любое сообщение
        bot.reply_to(message, "Не понимаю вашу команду")
        bot.send_message(
            user_id,
            "Нажимай на кнопки в меню и я предложу тебе фильмы/сериалы по твоему запросу",
        )

    elif state == "choosing_date_of_history":
        # Команда Вывести историю запросов, этап Ввод даты

        try:
            date_of_history = parser.parse(message.text)
            formatted_date = date_of_history.strftime("%Y-%m-%d")
            print_history(user_id, formatted_date)

            users_state[user_id].machine.final()

        except ValueError:
            bot.reply_to(message, "Неверный формат даты")
            bot.reply_to(message, "За какую дату вывести историю запросов?")
