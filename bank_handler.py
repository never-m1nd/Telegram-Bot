import requests
from collections import Counter


class ExchangeRate:

    def __init__(self, currency="USD", city="Минск"):
        self.url = 'https://belarusbank.by/api/kursExchange'
        self.currency = currency
        self.city = city

    def get_cities(self):
        response = requests.get(self.url)
        cities = set()
        for exchange_bureau in response.json():
            if exchange_bureau["name_type"] != "трасса":
                cities.add(exchange_bureau['name'])
        return cities

    def get_currencies(self):
        response = requests.get(self.url)
        print(response.json())
        currencies = []
        for key in response.json()[0]:
            if 'in' in key and len(key) == 6:
                currencies.append(key[:-3])
        return currencies

    def get_exchange_rate(self):
        payload = {'city': self.city}
        response = requests.get(self.url, params=payload)
        currency_in = []
        currency_out = []
        for exchange_bureau in response.json():
            currency_in.append(float(exchange_bureau[f'{self.currency}_in']))
            currency_out.append(float(exchange_bureau[f'{self.currency}_out']))
        currency_in = Counter(currency_in)
        currency_out = Counter(currency_out)
        rate = f'{currency_in.most_common(1)[0][0]:.4f}', f'{currency_out.most_common(1)[0][0]:.4f}'
        return rate

    def change_city(self, new_city):
        self.city = new_city

    def change_currency(self, new_currency):
        self.currency = new_currency

    def get_output(self, rate):
        return f"Продажа - {rate[0]}\nПокупка - {rate[1]}"

