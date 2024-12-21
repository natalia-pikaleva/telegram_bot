
from database.common.models import History, db
from database.core import crud
from site_API.core import site_api, url, headers
from settings import bot
import handlers
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()


#
# #Создание запроса и вывод истории запросов на экран
# db_write = crud.create()
# db_read = crud.retrieve()
#
# movie = site_api.get_movie()
#
# movie_name = 'Красотка'
# response = movie('GET', url, headers, movie_name, 5)
# response = response.json()
#
# data = [{'movie_name': movie_name, 'message': response.get('docs')}]
#
# # db_write(db, History, data)
# #
# # retrieved = db_read(db, History, History.movie_name, History.message)
# #
# # for element in retrieved:
# #     print(element.movie_name, element.message)
