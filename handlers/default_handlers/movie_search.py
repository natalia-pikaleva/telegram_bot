from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


@bot.message_handler(commands=["movie_search"])
def bot_find_movie(message: Message) -> None:
    """
    Функция получает на входе команду "movie_search" и переключает состояние
    пользователя на "choosing_movie_name"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_movie_name()
    bot.reply_to(message, "Введите название фильма")


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
        try:
            info_movie[key] = movie_total_info[key]
        except KeyError:
            info_movie[key] = ""

    return info_movie


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
