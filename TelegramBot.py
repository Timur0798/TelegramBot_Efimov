import telebot
import requests


TOKEN = "7177889986:AAHN7_vhXglbEyDlGSXSQY2fq40-25lZ_zE"
chat_id="5425211469"
mybot = telebot.TeleBot(TOKEN)

instruction="ИНСТРУКЦИЯ"

keys={"рубль":"RUB",
      "доллар":"USD",
      "евро":"EUR"
      }

@mybot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    text=f"Здравствуй, {name}!\n {instruction}"
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




mybot.polling(none_stop=True)