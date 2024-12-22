from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state

import json


def get_movie_info(movie_total_info: dict):
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


def search_movies(movie_name, genre, count_movies):
    data = []
    movie = site_api.get_movie()

    response = movie("GET", url, headers, movie_name, 5)
    response = response.json()

    count = 0

    for index_movie in range(len(response["docs"])):
        if count >= count_movies:
            return data

        genres_i_movie = response["docs"][index_movie]["genres"]
        for i_genre in genres_i_movie:
            if i_genre["name"] == genre:
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
        movie_name = message.text.capitalize()
        info_for_find["movie_name"] = movie_name
        bot.reply_to(message, "Введите жанр фильма")
        users_state[user_id].machine.choose_movie_genre()

    elif state == "choosing_movie_genre":
        movie_genre = message.text.lower()
        info_for_find["movie_genre"] = movie_genre
        bot.reply_to(message, "Введите количество фильмов для вывода")
        users_state[user_id].machine.choose_count_movies()

    elif state == "choosing_count_movies":
        try:
            count_movies = int(message.text)
            info_for_find["count_movies"] = count_movies
            users_state[user_id].machine.final()

            data = search_movies(
                movie_name=info_for_find["movie_name"],
                genre=info_for_find["movie_genre"],
                count_movies=info_for_find["count_movies"],
            )

            for index_movie in range(len(data)):
                bot.reply_to(
                    message, 'Информация о фильме "{}":'.format(index_movie + 1)
                )

                bot.reply_to(message, "Название: {}".format(data[index_movie]["name"]))
                bot.reply_to(
                    message,
                    "Описание: {}".format(data[index_movie]["description"]),
                )
                bot.reply_to(
                    message,
                    "Рейтинг: {}".format(data[index_movie]["rating"]),
                )
                bot.reply_to(message, "Год: {}".format(data[index_movie]["year"]))

                genres = ", ".join(
                    [i_genre["name"] for i_genre in data[index_movie]["genres"]]
                )

                bot.reply_to(message, "Жанр: {}".format(genres))
                bot.reply_to(
                    message,
                    "Возрастной рейтинг: {}".format(data[index_movie]["ageRating"]),
                )
                bot.reply_to(message, "Постер: {}".format(data[index_movie]["poster"]))

        except Exception as ex:
            print(ex)
            bot.reply_to(message, "Количество фильмов должно быть числом")
            bot.reply_to(message, "Введите количество фильмов для получения информации")
