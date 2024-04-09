import telebot
from config import keys, TOKEN
from extensions import MoneyConverter, APIException

mybot = telebot.TeleBot(TOKEN)

instruction=("Для начала работы введите данные (без склонения) в следующем формате:\n<название валюты> <в какую валюту конвертировать>\
<количество валюты>\n<посмотреть список доступных валют /values>\n<помощь в работе /help>")

@mybot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    text=f"Здравствуйте, {name}!\n {instruction}"
    mybot.reply_to(message,text)


@mybot.message_handler(commands=["help"])
def help(message):
    mybot.reply_to(message,instruction)

# Список доступных для конвертации валют
@mybot.message_handler(["values"])
def values(message):
    text="Список доступных валют:"
    for item in keys.keys():
        text="\n".join((text,item, ))
    mybot.reply_to(message,text)

# основной рабочий модуль с динамической ссылкой
@mybot.message_handler(content_types=["text"])
def convertation(message):
    try:
        objects = message.text.split(" ")
        if len(objects) != 3:
            raise APIException("Вы ввели большее количество параметров")

        quote, base, amount = objects
        result=MoneyConverter.get_price(quote,base,amount)
    except APIException as e:
        mybot.reply_to(message,f"Ошибка при введении данных пользователем\n{e}")
    except Exception as e:
        mybot.reply_to(message,f"Не удалось выполнить команду\n{e}")
    else:
        text = f"Цена {amount} {quote} равна {float(amount)*result} {base}"
        mybot.reply_to(message, text)


mybot.polling(none_stop=True)