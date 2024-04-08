import telebot
import requests
import json

TOKEN = "7177889986:AAHN7_vhXglbEyDlGSXSQY2fq40-25lZ_zE"
chat_id="5425211469"
mybot = telebot.TeleBot(TOKEN)

instruction=("Для начала работы введите данные (без склонения) в следующем формате:\n<название валюты> <в какую валюту конвертировать>\
<количество валюты>\n<посмотреть список доступных валют /values>\n<помощь в работе /help>")

keys={"рубль":"RUB",
      "доллар":"USD",
      "евро":"EUR"
      }

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote=str,base=str,amount=str):
        if quote == base:
            raise APIException(f"Нельзя конвертировать валюту {base} саму в себя")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Неправильный ввод валюты {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Неправильный ввод валюты {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось распознать количество {amount}")

        getter = requests.get(f"https://v6.exchangerate-api.com/v6/f7a3baf2ae0567e776cf4972/pair/{quote_ticker}/{base_ticker}")
        result=json.loads(getter.content)["conversion_rate"]
        return result


@mybot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    text=f"Здравствуйте, {name}!\n {instruction}"
    mybot.reply_to(message,text)

@mybot.message_handler(commands=["help"])
def help(message):
    mybot.reply_to(message,instruction)

# f7a3baf2ae0567e776cf4972 для API www.exchangerate-api.com

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
    objects = message.text.split(" ")

    if len(objects) != 3:
        raise ("Вы ввели большее количество параметров")

    quote, base, amount = objects
    result=MoneyConverter.get_price(quote,base,amount)

    text = f"Цена {amount} {quote} равна {float(amount)*result} {base}"
    mybot.reply_to(message, text)


mybot.polling(none_stop=True)