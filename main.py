from telebot.types import Message
import keyboards
from loader import bot
import handlers


@bot.message_handler(commands=['lowprice'])
def lowprice_func(message: Message) -> None:
    """Функция - обработчик команды 'lowprice'"""
    mode = 'PRICE'
    command = message.text
    handlers.search_city(message=message,
                         sort_mode=mode,
                         command=command)


@bot.message_handler(commands=['highprice'])
def highprice_func(message: Message) -> None:
    """Функция - обработчик команды 'highprice'"""
    mode = 'PRICE_HIGHEST_FIRST'
    command = message.text
    handlers.search_city(message=message,
                         sort_mode=mode,
                         command=command)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_func(message: Message) -> None:
    """Функция - обработчик команды 'highprice'"""
    mode = 'PRICE_HIGHEST_FIRST'
    command = message.text
    handlers.search_city(message=message,
                         sort_mode=mode,
                         command=command)


@bot.message_handler(commands=['history'])
def history_func(message: Message) -> None:
    """Функция - обработчик команды 'history'"""
    handlers.history(message=message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message) -> None:
    """Функция - обработчик сообщений"""
    if message.text == "/start":
        bot.send_message(chat_id=message.chat.id,
                         text="Привет, я - бот для поиска отелей."
                              "\nНапиши /help, чтобы узнать что я умею.")

    elif message.text == "/help":
        bot.send_message(chat_id=message.chat.id,
                         text="Топ самых дешёвых отелей в городе (/lowprice).\n"
                              "Топ самых дорогих отелей в городе (/highprice).\n"
                              "Топ отелей, наиболее подходящих по цене и расположению от центра (/bestdeal)\n"
                              "Узнать историю поиска отелей (/history)",
                         parse_mode='html')
        bot.send_message(chat_id=message.chat.id,
                         text='Что для тебя сделать?',
                         reply_markup=keyboards.keyboard_help())

    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Я тебя не понимаю. Напиши /help.")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
