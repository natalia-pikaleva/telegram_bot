from datetime import datetime
from dateutil import parser


def convert_date(input_date):
    try:
        # Используем dateutil для парсинга даты
        parsed_date = parser.parse(input_date)
        # Форматируем дату в нужный формат
        formatted_date = parsed_date.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError:
        return "Неверный формат даты"


# Запрос ввода от пользователя
user_input = input("Введите дату: ")
result = convert_date(user_input)
print("Преобразованная дата:", result)
