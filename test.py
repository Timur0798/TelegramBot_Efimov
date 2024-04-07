import requests

r=requests.get("https://v6.exchangerate-api.com/v6/f7a3baf2ae0567e776cf4972/pair/EUR/RUB")
print(r.content)