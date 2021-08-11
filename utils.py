import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"невозможно перевести одинаковые валюты '{quote}'")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту{base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Неверно введено количество валюты '{amount}'")

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={keys[quote]}{keys[base]}&key=07059f5883149133630be153252a483a')
        total_base = json.loads(r.content)['data'][keys[quote] + keys[base]]
        return total_base
