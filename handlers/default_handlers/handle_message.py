from datetime import datetime
from dateutil import parser

from telebot.types import Message

from settings import bot

from states.models import users_state, add_user, get_state

from utils.set_bot_commands import send_message, search_movies_high_budget
from utils.set_bot_commands import search_movies_low_budget, print_history
from utils.set_bot_commands import search_movies_with_rating, search_movies


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
