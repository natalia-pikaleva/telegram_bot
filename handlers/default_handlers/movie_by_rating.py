from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


@bot.message_handler(
    func=lambda message: message.text == "Найти фильм/сериал по рейтингу"
)
def bot_find_movie(message: Message) -> None:
    """
    Функция получает на входе команду movie_by_rating и переключает состояние
    пользователя на "choosing_movie_rating"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_rating()
    bot.reply_to(message, "Введите рейтинг")


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
