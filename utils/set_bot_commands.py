from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS

from datetime import datetime
from dateutil import parser
import ast

from telebot.types import Message

from database.common.models import History, db

from settings import bot

from database.core import crud

from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


def set_default_commands(bot):
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])


db_write = crud.create()
db_read = crud.retrieve()


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
        "budget",
        "poster",
    ]
    info_movie = {}

    for key in info_keys:
        try:
            info_movie[key] = movie_total_info[key]
        except KeyError:
            info_movie[key] = ""

    return info_movie


def search_movies_high_budget(budget: int, count_movies: int) -> list:
    """
    Функция получает на входе параметры для поиска: budget - бюджет и count_movies - количество фильмов
    и возвращает список из словарей с информацией о фильмах, с бюджетом, больщим суммы
    budget, количество фильмов count_movies
    :param budget: бюджет фильма
    :param count_movies: количество фильмов
    :return: список из словарей с информацией о фильмах, с бюджетом, большим суммы
    budget, количество фильмов count_movies
    """
    data = []
    movie = site_api.get_movie()

    url_budget = "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=250&selectFields=name&selectFields=year&selectFields=budget&selectFields=rating&selectFields=ageRating&selectFields=genres&selectFields=description&selectFields=poster&budget.value="
    new_url = url_budget + str(budget) + "-1000000000"

    response = movie("GET", new_url, headers, 5)
    response = response.json()["docs"]

    sorted_movie_list = sorted(response, key=lambda x: x["budget"]["value"])

    count = 0
    for i_movie in sorted_movie_list:
        if count >= count_movies:
            break

        if i_movie["budget"]["value"] >= budget:
            movie_info = get_movie_info(i_movie)

            data.append(movie_info)
            count += 1

    return data


def search_movies_low_budget(budget: int, count_movies: int) -> list:
    """
    Функция получает на входе параметры для поиска: budget - бюджет и count_movies - количество фильмов
    и возвращает список из словарей с информацией о фильмах, с бюджетом, меньшим суммы
    budget, количество фильмов count_movies
    :param budget: бюджет фильма
    :param count_movies: количество фильмов
    :return: список из словарей с информацией о фильмах, с бюджетом, меньшим суммы
    budget, количество фильмов count_movies
    """
    data = []
    movie = site_api.get_movie()

    url_budget = "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=250&selectFields=name&selectFields=year&selectFields=budget&selectFields=rating&selectFields=ageRating&selectFields=genres&selectFields=description&selectFields=poster&budget.value="
    new_url = url_budget + "0-" + str(budget)

    response = movie("GET", new_url, headers, 5)
    response = response.json()["docs"]

    sorted_movie_list = sorted(response, key=lambda x: x["budget"]["value"])

    count = 0
    for i_movie in sorted_movie_list[::-1]:
        if count >= count_movies:
            break

        if i_movie["budget"]["value"] <= budget:
            movie_info = get_movie_info(i_movie)

            data.append(movie_info)
            count += 1

    return data


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

    bot.send_message(user_id, "История запросов за {}:".format(date))

    retrieved = db_read(db, History, History.date, History.movie_info)

    flag = True
    for element in retrieved:
        history_date = element.date

        if history_date == date:
            flag = False

            movies_list = ast.literal_eval(element.movie_info)

            for i_movie in movies_list:
                send_message_history(user_id, i_movie)

    if flag:
        bot.send_message(user_id, "На указанную дату не было запросов")


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

    response = response.json()["docs"]

    sorted_movie_list = sorted(response, key=lambda x: x["rating"]["kp"])

    count = 0
    for i_movie in sorted_movie_list:
        if count >= count_movie:
            break

        if float(i_movie["rating"]["kp"]) >= rating:
            movie_info = get_movie_info(i_movie)

            data.append(movie_info)
            count += 1

    return data


def search_movies(movie_name: str, genre: str, count_movies: int) -> list:
    """
    Функция получает на входе название фильма, его жанр и количество фильмов для
    вывода и возвращает список из словарей с информацией о фильмах, подходящих
    под заданные параметры
    :param movie_name: название фильма
    :param genre: жанр фильма
    :param count_movies: количество фильмов для вывода в чат бота
    :return: список из словарей с информацией о фильмах, подходящих
    под заданные параметры
    """
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
