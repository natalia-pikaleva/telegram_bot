import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", 'Найти информацию о фильме'),
    ('movie_by_rating', 'Найти фильм/сериал по рейтингу'),
    ('low_budget_movie', 'Найти фильм/сериал с низким бюджетом'),
    ('high_budget_movie', 'Найти фильм/сериал с высоким бюджетом'),
    ('history', 'Просмотр истории запросов')
)
