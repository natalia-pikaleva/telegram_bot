from telebot.types import Message
from settings import bot
from database.core import crud
from database.common.models import db, History


@bot.message_handler(commands=["history"])
def bot_history(message: Message):
    # db_read = crud.retrieve()
    # retrieved = db_read(db, History, History.movie_name, History.message)
    #
    # for element in retrieved:
    #     print(element.movie_name, element.message)

    bot.reply_to(message, "Запущен процесс вывода истории запросов")


if __name__ == "__main__":
    bot_history()
