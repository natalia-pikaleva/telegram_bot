from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from settings import bot


@bot.message_handler(func=lambda message: message.text == "Обо мне")
def bot_help(message: Message) -> None:
    """
    Функция получает на входе команду help и выводит в чат бота список доступных команд
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    bot.send_message(user_id, "Я бот по поиску фильмов")
    bot.send_message(
        user_id,
        "Нажимай на кнопки в меню и я предложу тебе фильмы/сериалы по твоему запросу",
    )
