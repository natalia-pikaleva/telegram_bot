from datetime import datetime
from telebot.types import Message

from database.common.models import History, db
from database.core import crud
from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state
from .start import db_write, db_read
import json


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


def get_movie_info(movie_total_info: dict) -> dict:
    """
    Функция получает на входе словарь с полной информацией о фильме и возвращает
    словарь с информацией по отобранным ключевым полям
    :param movie_total_info: словарь с полной информацией о фильме
    :return: словарь с информацией о фильме по конкретным ключевым полям
    """
    info_keys = [
        "name",
        "description",
        "rating",
        "year",
        "genres",
        "ageRating",
        "poster",
    ]
    info_movie = {}

    for key in info_keys:
        info_movie[key] = movie_total_info[key]

    return info_movie


def search_movies_with_rating(rating: float, count_movie: int) -> list:
    """
    Функция получает на входе рейтинг фильма rating и количество фильмов для вывода count_movies.
    Возвращает список фильмов с рейтингом от rating и выше в количестве count_movies
    :param rating: рейтинг фильма
    :param count_movie: количество фильмов
    :return: список фильмов с рейтингом от rating и выше в количестве count_movies
    """
    data = []
    movie = site_api.get_movie()

    new_url = url + "250" + "&rating.kp=" + str(rating) + "%20-%2010"

    response = movie("GET", new_url, headers, 5)
    response = response.json()

    count = 0
    for index_movie in range(min(len(response["docs"]), count_movie)):
        if count >= count_movie:
            return data
        movie_info = get_movie_info(response["docs"][index_movie])
        rating_i_movie = response["docs"][index_movie]["rating"]["kp"]
        if float(rating_i_movie) >= rating:
            data.append(movie_info)
            count += 1

    return data


def search_movies(movie_name, genre, count_movies):
    data = []
    movie = site_api.get_movie()

    new_url = url + str(count_movies) + "&query=" + movie_name

    response = movie("GET", new_url, headers, 5)
    response = response.json()

    for index_movie in range(len(response["docs"])):

        genres_i_movie = response["docs"][index_movie]["genres"]
        for i_genre in genres_i_movie:
            if i_genre["name"] == genre:
                movie_info = get_movie_info(response["docs"][index_movie])
                data.append(movie_info)

    return data


def search_movies_low_budget(budget, count_movies):
    data = []
    movie = site_api.get_movie()

    new_url = url + "250" + "&budget.value=0" + str(budget)

    response = movie("GET", new_url, headers, 5)
    response = response.json()

    count = 0
    for index_movie in range(len(response["docs"])):
        if count >= count_movies:
            return data

        movie_info = get_movie_info(response["docs"][index_movie])

        data.append(movie_info)
        count += 1

    return data


@bot.message_handler(content_types=["text"])
def handle_message(message: Message, info_for_find={}):
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

    elif state == "start":
        # Состояние Старт - пользователь отправил любое сообщение
        bot.reply_to(message, "Не понимаю вашу команду")
        bot.send_message(
            user_id,
            "Нажмите на кнопку help в меню, чтобы узнать доступные запросы",
        )
