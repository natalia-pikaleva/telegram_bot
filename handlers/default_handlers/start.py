from telebot.types import Message

from settings import bot


from states.models import users_state, add_user, get_state

from database.core import crud

from keyboards.reply.core import create_menu

db_write = crud.create()
db_read = crud.retrieve()


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Функция получает на входе команду start и реализует кнопки меню с командами
    :param message: сообщение пользователя
    """
    user_id = message.chat.id
    if not user_id in users_state:
        add_user(user_id)

    bot.reply_to(
        message,
        "Привет, {}! Я бот по поиску фильмов. Чтобы выполнить запрос, нажимай на кнопки меню".format(
            message.from_user.full_name
        ),
        reply_markup=create_menu(),
    )

    if get_state(user_id) != "start":
        users_state[user_id].machine.cancel()
