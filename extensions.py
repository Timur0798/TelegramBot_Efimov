import requests
import json
from config import keys

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