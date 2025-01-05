from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS

from datetime import datetime
from dateutil import parser
import ast

from telebot.types import Message


from settings import bot

from database.core import crud

from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


def set_default_commands(bot):
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])


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
