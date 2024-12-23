from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from settings import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
    Функция получает на входе команду help и выводит в чат бота список доступных команд
    :param message: сообщение пользователя
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
