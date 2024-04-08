import requests
import json

message=input("Введите:")
keys={"рубль":"RUB",
      "доллар":"USD",
      "евро":"EUR"
      }
quote,base,quantity=message.split(" ")

getter=requests.get(f"https://v6.exchangerate-api.com/v6/f7a3baf2ae0567e776cf4972/pair/{keys[quote]}/{keys[base]}")
a=json.loads(getter.content)["conversion_rate"]
print(a)