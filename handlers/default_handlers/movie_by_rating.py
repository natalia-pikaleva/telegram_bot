from telebot.types import Message

from settings import bot

from states.models import users_state, add_user, get_state


@bot.message_handler(
    func=lambda message: message.text == "Найти фильм/сериал по рейтингу"
)
def bot_find_movie(message: Message) -> None:
    """
    Функция получает на входе команду movie_by_rating и переключает состояние
    пользователя на "choosing_movie_rating"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_rating()
    bot.reply_to(message, "Введите рейтинг")
