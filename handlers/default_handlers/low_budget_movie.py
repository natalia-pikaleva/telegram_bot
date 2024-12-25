from telebot.types import Message

from settings import bot

from states.models import users_state, add_user, get_state


@bot.message_handler(
    func=lambda message: message.text == "Найти фильм/сериал с низким бюджетом"
)
def bot_low_budget_movie(message: Message) -> None:
    """
    Функция получает на входе команду low_budget_movie и переключает состояние
    пользователя на "choosing_low_budget_movie"
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()

    users_state[user_id].machine.choose_low_budget()
    bot.reply_to(message, "Введите сумму бюджета для поиска фильмов")
