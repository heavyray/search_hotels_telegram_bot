import main
import rapidapi
from telebot.types import Message, InputMediaPhoto, CallbackQuery

from DB_services.db_services import save_search, get_history, get_hotels
from loader import bot
import keyboards
from user import user_dict, User


def search_city(message: Message, sort_mode: str, command: str) -> None:
    """Поиск города"""
    chat_id = message.chat.id
    user_dict[chat_id] = User(sort_order=sort_mode, command=command)

    msg = bot.send_message(chat_id=chat_id,
                           text="В каком городе будем искать?",
                           reply_markup=keyboards.delete_keyboard())

    bot.register_next_step_handler(msg, check_in)


def check_in(message: Message) -> None:
    """Выбор даты заселения"""
    chat_id = message.chat.id
    user = user_dict[chat_id]

    try:

        if message.text.lower() == 'стоп':
            message.text = '/help'
            main.get_text_messages(message=message)
            return

        elif message.text.isalpha():
            rapidapi.search_city(city=message.text,
                                 user=user)

            calendar = keyboards.create_calendar()
            bot.send_message(chat_id=chat_id,
                             text="Выберете дату заезда",
                             reply_markup=calendar)

        else:
            raise TypeError

    except TypeError:
        msg = bot.send_message(chat_id=chat_id,
                               text='Некорректное название города, попробуй еще раз\n'
                                    'Если хочешь закончить напиши Стоп.',
                               parse_mode='html')
        bot.register_next_step_handler(msg, check_in)


def check_out(message: Message) -> None:
    """Выбор даты выселения"""
    chat_id = message.chat.id
    calendar = keyboards.create_calendar()

    bot.send_message(chat_id=chat_id,
                     text="Выберете дату выезда",
                     reply_markup=calendar)


@bot.callback_query_handler(func=keyboards.callback_func())
def callback_calendar_handler(call: CallbackQuery):
    """Обработчик выбора дат"""
    chat_id = call.message.chat.id
    user = user_dict[chat_id]

    bot.answer_callback_query(callback_query_id=call.id)

    text = 'выезда'
    if user_dict[chat_id].check_in is None:
        text = 'заезда'

    result, key, step = keyboards.second_calendar(data=call.data)

    if not result and key:
        bot.edit_message_text(text=f"Выберете дату {text}",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=key)

    elif result:
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)

        if user.check_in is None:
            user.check_in = result
            check_out(message=call.message)

        elif user.check_in is not None and user.check_out is None:
            user.check_out = result

            if (user.check_out - user.check_in).days <= 0:

                bot.send_message(chat_id=chat_id,
                                 text='Неверно указаны даты, необходимо, чтобы дата выселения\n'
                                      'была позднее даты заселения как минимум на один день.')

                user.check_in = None
                user.check_out = None

                calendar = keyboards.create_calendar()
                bot.send_message(chat_id=chat_id,
                                 text="Выберете дату заезда",
                                 reply_markup=calendar)

            else:
                if user.sort_order == 'PRICE_HIGHEST_FIRST' and user.command == '/bestdeal':
                    msg = bot.send_message(chat_id=chat_id,
                                           text='Введите желаемую стоимость за сутки.\n'
                                                'Через пробел минимальную и максимальную.',
                                           parse_mode='html')
                    bot.register_next_step_handler(msg, choose_price)

                else:
                    kb = keyboards.choose_city(city_dict=user.city_dict)
                    bot.send_message(chat_id=chat_id,
                                     text='Отлично, теперь нужно уточнить город.',
                                     reply_markup=kb)


def choose_price(message: Message) -> None:
    """Ввод цены за отель"""
    chat_id = message.chat.id
    user = user_dict[chat_id]
    price_list = message.text.split(' ')

    try:
        if message.text.lower() == 'стоп':
            message.text = '/help'
            main.get_text_messages(message=message)
            return

        elif len(price_list) != 2 or not all([num.isdigit() for num in price_list]) or price_list[0] > price_list[1]:
            raise ValueError

        user.price_min = price_list[0]
        user.price_max = price_list[1]

        msg = bot.send_message(chat_id=chat_id,
                               text='Введите целым числом максимальную удаленность отеля от центра города.')
        bot.register_next_step_handler(msg, choose_distance)

    except ValueError:
        msg = bot.send_message(chat_id=chat_id,
                               text='Неверный формат ввода.\n'
                                    'Нужно ввести минимальную и максимальную цену за сутки через пробел.\n'
                                    'Если хочешь закончить напиши Стоп.',
                               parse_mode='html')
        bot.register_next_step_handler(msg, choose_price)


def choose_distance(message: Message) -> None:
    """Ввод желаемой удаленности отеля от центра"""
    chat_id = message.chat.id
    user = user_dict[chat_id]
    max_distance = message.text

    try:
        if message.text.lower() == 'стоп':
            message.text = '/help'
            main.get_text_messages(message=message)
            return

        elif not max_distance.isdigit():
            raise ValueError

        user.max_distance = int(max_distance)
        kb = keyboards.choose_city(city_dict=user.city_dict)
        bot.send_message(chat_id=chat_id,
                         text='Отлично, теперь нужно уточнить город.',
                         reply_markup=kb)

    except ValueError:
        msg = bot.send_message(chat_id=chat_id,
                               text='Неверный формат ввода.\n'
                                    'Нужно ввести максимальную дистанцию целым числом.\n'
                                    'Если хочешь закончить напиши Стоп.',
                               parse_mode='html')
        bot.register_next_step_handler(msg, choose_distance)


@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_city-'))
def callback_search_city(call: CallbackQuery) -> None:
    """Обработчик уточнения города"""
    chat_id = call.message.chat.id
    user = user_dict[chat_id]
    city_id = int(call.data.replace('choose_city-', ''))
    user.city_name = user.city_dict[city_id]

    bot.answer_callback_query(callback_query_id=call.id)
    bot.delete_message(chat_id=chat_id,
                       message_id=call.message.message_id)

    user.city_id = city_id
    kb = keyboards.count_photo()
    bot.send_message(chat_id=chat_id,
                     text='Сколько фотографий отеля прикреплять?',
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.startswith('count_photo-'))
def callback_count_photo(call: CallbackQuery) -> None:
    """Обработчик необходимости вывода фото отелей"""
    chat_id = call.message.chat.id
    user = user_dict[chat_id]

    count_photo = int(call.data.replace('count_photo-', ''))

    bot.answer_callback_query(callback_query_id=call.id)
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    last_msg = bot.send_message(chat_id=chat_id,
                                text='Секундочку, ищу')

    if count_photo != 0:
        user.photo = True
        user.count_photo = count_photo

    rapidapi.search_hotel(user=user)
    bot.delete_message(chat_id=chat_id,
                       message_id=last_msg.message_id)

    if len(user.hotels_list) == 0:
        bot.send_message(chat_id=chat_id,
                         text='Не удалось найти ни одного отеля по заданным параметрам.\n'
                              'Возвращаю вас в главное меню.',
                         parse_mode='html',
                         timeout=3)

        call.message.text = '/help'
        main.get_text_messages(message=call.message)
        return

    msg = bot.send_message(chat_id=chat_id,
                           text=f"Мне удалось найти {len(user.hotels_list)} отелей.\n"
                                f"Сколько вывести для Вас?",
                           parse_mode='html')
    bot.register_next_step_handler(msg, choose_count_hotel)


def choose_count_hotel(message: Message) -> None:
    """Ввод количества выводимых отелей"""
    chat_id = message.chat.id
    user = user_dict[chat_id]

    try:

        if message.text.lower() == 'стоп':
            message.text = '/help'
            main.get_text_messages(message=message)
            return

        elif not message.text.isdigit():
            raise ValueError

        elif int(message.text) == 0 or int(message.text) > len(user.hotels_list):
            raise ValueError

        user.hotels_list = user.hotels_list[:int(message.text)]
        print_hotel_info(chat_id=chat_id,
                         user=user)
    except ValueError:
        msg = bot.send_message(chat_id=chat_id,
                               text=f'Попробуй ввести число от 1 до {user.count_hotels}.\n'
                                    f'Если хочешь закончить напиши Стоп.')
        bot.register_next_step_handler(msg, choose_count_hotel)


def print_hotel_info(chat_id: int, user: User) -> None:
    """Отправка результатов поиска пользователю"""
    hotels_list = user.hotels_list
    for i_hotel in hotels_list:
        bot.send_message(chat_id=chat_id,
                         text=i_hotel,
                         reply_markup=keyboards.hotels_url(i_hotel.url),
                         parse_mode='html')
        if user.photo:
            media_group = list()

            for i_number, url in enumerate(i_hotel.photo_list):
                media_group.append(InputMediaPhoto(media=url))

            bot.send_media_group(chat_id=chat_id,
                                 media=media_group)

    save_search(chat_id=chat_id,
                command=user.command,
                city=user.city_name,
                hotels_list=hotels_list)


def history(message: Message):
    """Вывод последних запросов пользователя"""
    chat_id = message.chat.id
    result = get_history(chat_id)
    if not result:
        bot.send_message(
            chat_id=chat_id,
            text='История поиска пуста',
            reply_markup=keyboards.delete_keyboard()
        )
        return

    kb = keyboards.history_kb(result)
    bot.send_message(
        chat_id=chat_id,
        text='Вот что вы искали в последнее время:',
        reply_markup=kb
    )


def get_history_info(data_list: list) -> str:
    """Возвращает строку с информацией об отеле"""
    return f"Отель {data_list[1]}" \
           f"\nКласс: {data_list[2]} &#9733;" \
           f"\nАдрес: {data_list[3]}" \
           f"\nЦена за {data_list[6]} ночей: {data_list[4]}руб" \
           f"\nЦена за ночь: {round(data_list[4] / data_list[6])}руб" \
           f"\nРасстояние до центра города: {data_list[5]} км"


@bot.callback_query_handler(func=lambda call: call.data.startswith('history'))
def callback_search_city(call: CallbackQuery) -> None:
    """Обработчик выбора истории запросов"""
    chat_id = call.message.chat.id
    bot.answer_callback_query(callback_query_id=call.id)
    bot.delete_message(chat_id=chat_id,
                       message_id=call.message.message_id)

    search_id = int(call.data.replace('history-', ''))
    result = get_hotels(search_id)

    for i_hotel in result:
        bot.send_message(chat_id=chat_id,
                         text=get_history_info(i_hotel),
                         reply_markup=keyboards.hotels_url(i_hotel[7]),
                         parse_mode='html')
