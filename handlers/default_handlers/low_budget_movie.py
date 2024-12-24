from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


@bot.message_handler(commands=["low_budget_movie"])
def bot_low_budget_movie(message: Message) -> None:
    """
    Функция получает на входе команду low_budget_movie и переключает состояние
    пользователя на "choosing_low_budget_movie"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_low_budget()
    bot.reply_to(message, "Введите сумму бюджета для поиска фильмов")


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
