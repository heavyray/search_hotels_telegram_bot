from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import WYearTelegramCalendar


def keyboard_help() -> ReplyKeyboardMarkup:
    """Клавиатура с основными командами"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    key_lowprice = InlineKeyboardButton(text='/lowprice', callback_data='lowprice')
    key_highprice = InlineKeyboardButton(text='/highprice', callback_data='highprice')
    key_bestdeal = InlineKeyboardButton(text='/bestdeal', callback_data='bestdeal')
    key_history = InlineKeyboardButton(text='/history', callback_data='history')
    keyboard.row(key_lowprice, key_highprice)
    keyboard.row(key_bestdeal, key_history)

    return keyboard


def delete_keyboard() -> ReplyKeyboardRemove:
    """Убирает клавиатуру"""
    return ReplyKeyboardRemove()


def choose_city(city_dict: dict) -> InlineKeyboardMarkup:
    """Клавиатура с городами"""
    keyboard = InlineKeyboardMarkup()
    for id_city, name_city in city_dict.items():
        key = InlineKeyboardButton(text=name_city, callback_data=f'choose_city-{id_city}')
        keyboard.add(key)

    return keyboard


def hotels_url(url: str) -> InlineKeyboardMarkup:
    """Кнопка перехода на страницу бронирования отеля"""
    keyboard = InlineKeyboardMarkup()
    key = InlineKeyboardButton(text='Перейти на страницу отеля', url=url)
    keyboard.add(key)

    return keyboard


def create_calendar() -> WYearTelegramCalendar:
    """"""
    calendar, step = WYearTelegramCalendar(locale="ru").build()

    return calendar


def second_calendar(data) -> WYearTelegramCalendar:
    """"""
    return WYearTelegramCalendar(locale='ru').process(data)


def callback_func():
    """"""
    return WYearTelegramCalendar.func()


def count_photo() -> InlineKeyboardMarkup:
    """Клавиатура для выбора количества фото"""
    keyboard = InlineKeyboardMarkup(row_width=5)
    cb_data = f'count_photo-'
    keyboard.add(InlineKeyboardButton(text='Не нужно выводить фотографии',
                                      callback_data=cb_data+'0'))

    for num in [1, 6]:
        keyboard.row(InlineKeyboardButton(text=str(num), callback_data=cb_data+f'{num}'),
                     InlineKeyboardButton(text=str(num + 1), callback_data=cb_data+f'{num+1}'),
                     InlineKeyboardButton(text=str(num + 2), callback_data=cb_data+f'{num+2}'),
                     InlineKeyboardButton(text=str(num + 3), callback_data=cb_data+f'{num+3}'),
                     InlineKeyboardButton(text=str(num + 4), callback_data=cb_data+f'{num+4}'))

    return keyboard


def history_kb(searches_list: list) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для выбора запроса из истории поиска"""
    keyboard = InlineKeyboardMarkup()

    for search in searches_list:
        text = f'{search[3]}, команда: {search[2]}'
        cb_data = f'history-{search[0]}'
        key = InlineKeyboardButton(text=text, callback_data=cb_data)
        keyboard.add(key)

    return keyboard
