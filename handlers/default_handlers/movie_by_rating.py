from telebot.types import Message

from settings import bot
from site_API.core import site_api, url, headers

from states.models import users_state, add_user, get_state


@bot.message_handler(commands=["movie_by_rating"])
def bot_find_movie(message: Message):
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_rating()
    bot.reply_to(message, "Введите рейтинг")
