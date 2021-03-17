# Import library for working with checking weather
import pyowm
from pyowm.utils.config import get_default_config

# Import config
from Configs.configure import weather_api


def get_curr_weather(city):
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = pyowm.OWM(weather_api, config_dict)

        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather

        # погодные характеристики
        pressure = str(w.pressure['press'] * 0.75) + ' мм.рт.ст'
        weather_now = w.detailed_status
        temp = str(w.temperature('celsius')['temp']) + '°C'
        max_temp = str(w.temperature('celsius')['temp_max']) + '°C'
        min_temp = str(w.temperature('celsius')['temp_min']) + '°C'
        temp_feels = str(w.temperature('celsius')['feels_like']) + '°C'
        wind = str(w.wind()['speed']) + ' м/с'
        humid = str(w.humidity) + ' %'

        return f'🌤В городе {city} сейчас {weather_now}' \
               f'\n🌡Температура воздуха: {temp}' \
               f'\n🌡Температура воздуха: {temp}' \
               f'\n🌡[max]Максимальная температура воздуха: {max_temp}' \
               f'\n🌡[min]Минимальная температура воздуха: {min_temp}' \
               f'\n🌡[+-]Ощущается: {temp_feels}' \
               f'\n\n💨Скорость ветра: {wind}' \
               f'\n💧Влажность: {humid}' \
               f'\n🌀Атмосферное давление: {pressure}'

    except:

        return f'Извините, город {city} отсутствует в моей базе данных' \
               f'\nили вы неправильно ввели название города☹'
