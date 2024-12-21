# from loader import bot
# import handlers  # noqa
# from utils.set_bot_commands import set_default_commands
#
# if __name__ == "__main__":
#     set_default_commands(bot)
#     bot.infinity_polling()
#
from database.core import crud
from site_API.core import site_api, url, headers

db_write = crud.create()
db_read = crud.retrieve()

movie = site_api.get_movie()

response = movie('GET', url, headers, 'Красотка', 5)
response = response.json()

print(response)