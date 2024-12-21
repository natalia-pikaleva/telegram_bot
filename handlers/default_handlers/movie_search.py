
from telebot.types import Message

from database.common.models import db, History
from settings import bot

from database.core import crud
from site_API.core import site_api, url, headers

import json


@bot.message_handler(commands=["movie_search"])
def bot_find_movie(message: Message):
    bot.reply_to(message, "Введите название фильма")

def get_movie_info(movie_total_info: dict):
    info_keys = ["name", "description", "rating",  "year", "genres", "ageRating", "poster"]
    info_movie = {}

    for key in info_keys:
        info_movie[key] = movie_total_info[key]

    return info_movie

def search_movies(movie_name, genre):
    data = []
    movie = site_api.get_movie()

    response = movie('GET', url, headers, movie_name, 5)
    response = response.json()

    for index_movie in range(len(response['docs'])):
        genres_i_movie = response['docs'][index_movie]['genres']
        for i_genre in genres_i_movie:
            if i_genre['name'] == genre:
                movie_info = get_movie_info(response["docs"][index_movie])

                data.append({'movie_name': movie_name, 'message': movie_info})

    return data

@bot.message_handler(content_types=['text'])
def handle_text(message, user_data=[], count = 0):
    if len(user_data) == 0:
        user_data.append(message.text)
        bot.reply_to(message, "Введите жанр")

    elif len(user_data) == 1:
        user_data.append(message.text)
        movie_name = user_data[0].capitalize()
        genre = user_data[1].lower()


        data = search_movies(movie_name, genre)

        if len(data) != 0:
            with open('data.json', 'w', encoding='utf-8') as data_file:
                json.dump(data, data_file, ensure_ascii=False, indent=4)

            bot.reply_to(message, "Найдено {} вариантов с такими параметрами, сколько вариантов вывести?".format(
                len(data)
            ))
        else:
            bot.reply_to(message, 'Фильмы с такими параметрами не найдены')
            user_data.clear()

    elif count == 0:

        try:
            count = int(message.text)

            with open('data.json', 'r', encoding='utf-8') as data_file:
                data = json.load(data_file)

            db_write = crud.create()


            db_write(db, History, data)

            for index_movie in range(min(len(data), count)):
                bot.reply_to(message, 'Информация о фильме "{}":'.format(index_movie + 1))

                bot.reply_to(message, 'Название: {}'.format(data[index_movie]["message"]['name']))
                bot.reply_to(message, 'Описание: {}'.format(data[index_movie]["message"]['description']))
                bot.reply_to(message, 'Рейтинг: {}'.format(data[index_movie]["message"]['rating']))
                bot.reply_to(message, 'Год: {}'.format(data[index_movie]["message"]['year']))

                genres = ', '.join([i_genre['name'] for i_genre in data[index_movie]["message"]['genres']])

                bot.reply_to(message, 'Жанр: {}'.format(genres))
                bot.reply_to(message, 'Возрастной рейтинг: {}'.format(data[index_movie]["message"]['ageRating']))
                bot.reply_to(message, 'Постер: {}'.format(data[index_movie]["message"]['poster']))

            user_data.clear()
            count = 0

        except Exception:
            bot.reply_to(message, "Количество вариантов для вывода должно быть числом")
            bot.reply_to(message, "Введите количество вариантов для вывода")




