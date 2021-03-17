#from bot.telegram_bot import Weather_bot
from data.configure import weather_api, TG_token


import telebot
import requests


class Forecast():
    def __init__(self, city, bot):
        super().__init__(bot)

        self.city = city
        self.get_city_id(self.city)

    def get_city_id(self, city):
        
        try:
            get_data = requests.get(
                "http://api.openweathermap.org/data/2.5/find",
                params = {
                    'q': city,
                    'type': 'like',
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': weather_api
                }
            )

            data = get_data.json()
            for d in data['list']:
                self.cities = "{} ({})".format(d['name'], d['sys']['country'])
                
                print(self.cities)

        except:

            return f'К сожалению, город {city} отсутствует в моей базе данных или вы неправильно ввели название города'


