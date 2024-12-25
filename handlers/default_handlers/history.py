from telebot.types import Message
from settings import bot

from states.models import users_state, add_user, get_state


@bot.message_handler(func=lambda message: message.text == "Просмотр истории запросов")
def bot_history(message: Message) -> None:
    """
    Функция получает на входе команду history и переключает состояние
    пользователя на choosing_date_of_history
    :param message: сообщение пользователя
    """

    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_date_of_history()
    bot.reply_to(
        message,
        "За какую дату вывести историю запросов?",
    )
