from telebot.types import Message

from settings import bot

from states.models import users_state, add_user, get_state

from database.core import crud

db_write = crud.create()
db_read = crud.retrieve()


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    bot.reply_to(
        message,
        f"Привет, {message.from_user.full_name}! Я бот по поиску фильмов. Чтобы узнать доступные запросы, нажмите на кнопку help в меню",
    )
