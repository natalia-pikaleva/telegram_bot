from telebot.types import Message

from settings import bot

from states.models import users_state, add_user, get_state


@bot.message_handler(
    func=lambda message: message.text == "Найти информацию о фильме/сериале"
)
def bot_find_movie(message: Message) -> None:
    """
    Функция получает на входе команду "movie_search" и переключает состояние
    пользователя на "choosing_movie_name"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_movie_name()
    bot.reply_to(message, "Введите название фильма")
