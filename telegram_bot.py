#Импорт необходимых переменных для работы с базой данных
from configure import TG_token, weather_api
from add_info import db, remove_users, search_users, save_users, take_user_time, take_user_city
#Импорт библиотеки и ее функций для работы с ботом
import telebot
from telebot.types import Message
from telebot import types
#Импорт библиотеки для работы с функцией отслеживания погоды
import pyowm
from pyowm.utils.config import get_default_config
#Другие необходимые библиотеки
import datetime
import schedule
import time

class Weather_bot:
    def __init__(self, bot):
        self.bot = bot

        self.func_commands()
        self.func_weather()
    
    #основные комманды
    def func_commands(self):
        @self.bot.message_handler(func = lambda message: True, commands=['start', 'info'], content_types = ['text'])
        def main(message):

            self.user_id = message.from_user.id
            self.message_chat_id = message.chat.id
            
            #Кастомная клавиатура для настройки рассылки
            sub_fc_key = types.ReplyKeyboardMarkup(resize_keyboard = True)
            take_sub_fc_button = types.KeyboardButton(text='Подписаться на рассылку погоды')
            take_unsub_fc_button = types.KeyboardButton(text='Отписаться от рассылки погоды')
            sub_fc_key.row(take_sub_fc_button, take_unsub_fc_button)

            if message.text == '/start':
                
                self.bot.send_message( message.chat.id, f'Привет, {message.from_user.first_name}, я бот, призванный облегчить наблюдение за погодой😉.'
                + '\nНапиши мне свой город и я расскажу, всё что знаю о нём.\nВведите команду /info, если что-то непонятно))', reply_markup = sub_fc_key )

                self.forecast_commands()

            elif message.text == '/info':
                self.inline_info_key = types.InlineKeyboardMarkup()
                self.inline_info_button1 = types.InlineKeyboardButton(text='Что ты умеешь?', callback_data = 'aboutbot')
                self.inline_info_button2 = types.InlineKeyboardButton(text='Как запросить погоду?', callback_data = 'howWeather')
                self.inline_info_key.add(self.inline_info_button1, self.inline_info_button2)

                self.bot.send_message(message.chat.id, 'Что вы хотите узнать обо мне?', reply_markup=self.inline_info_key)

                self.callback()
                
    def callback(self):
        @self.bot.callback_query_handler(func = lambda call: True)
        def request_callback(call):
            
            if call.data == 'aboutbot':

                self.bot.send_message(call.message.chat.id, 'Я могу узнать текущую погоду вашего города.'
                + 'Всё просто, вы пишите мне свой город, а я обрабатываю запрос с помощью Python и его библиотеки pyowm, получаю результат и отправляю его вам.😉 ')

            elif call.data == 'howWeather':
                self.bot.send_message(call.message.chat.id, 'Узнать погоду можно, вызвав команду /weather')


    def forecast_commands(self):
        @self.bot.message_handler(content_types = ['text'])
        def comm(message):

            if message.text == 'Подписаться на рассылку погоды':
                check_subscribe = search_users(db, user_id = self.user_id)

                if check_subscribe == False:
                    city_input = self.bot.send_message(message.chat.id, 'Город?')
                    self.bot.register_next_step_handler(city_input, self.set_city)


                elif check_subscribe == True:
                    self.bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку. Если хотите изменить данные, отправьте "cd".')

            elif message.text == 'Отписаться от рассылки погоды':
                self.bot.send_message(message.chat.id, remove_users(db, user_id = self.user_id))

    def get_id(self):
        self.user_id = None
        @self.bot.message_handler()
        def g(message):
            self.user_id = message.from_user.id
            return self.user_id

    def set_city(self, message):
        self.city = message.text
            
        time_input = self.bot.send_message(message.chat.id, 'Время отправки прогноза? (чч:мм)')
        self.bot.register_next_step_handler(time_input, self.set_time)

    def set_time(self, message):
        self.time = message.text
        
        self.save_sub()

    def save_sub(self):

        save_users(db, user_id = self.user_id, time = self.time, city = self.city)
        self.bot.send_message(self.user_id, 'Вы успешно подписались на рассылку!😎')

        self.send_forecast()
        

    def send_forecast(self):
        def daily_forecast():
            try:
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = pyowm.OWM(weather_api, config_dict)
                                        
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(take_user_city(db, user_id = self.user_id))
                w = observation.weather

                        #погодные характеристики
                pressure = str(w.pressure['press'] * 0.75) + ' мм.рт.ст'
                weather_now = w.detailed_status
                temp = str(w.temperature('celsius')['temp']) + '°C'
                max_temp = str(w.temperature('celsius')['temp_max']) + '°C'
                min_temp = str(w.temperature('celsius')['temp_min']) + '°C'
                temp_feels = str(w.temperature('celsius')['feels_like']) + '°C'
                wind = str(w.wind()['speed']) + ' м/с'
                humid = str(w.humidity) + ' %'

                self.bot.send_message(self.message_chat_id,

                f'🌤В городе {self.city} сейчас {weather_now}'
                + f'\n🌡Температура воздуха: {temp}'
                + f'\n🌡[max]Максимальная температура воздуха: {max_temp}'
                + f'\n🌡[min]Минимальная температура воздуха: {min_temp}'
                + f'\n🌡[+-]Ощущается: {temp_feels}'
                + f'\n\n💨Скорость ветра: {wind}'
                + f'\n💧Влажность: {humid}'
                + f'\n🌀Атмосферное давление: {pressure}'
                )

            except:
                self.bot.send_message(self.message_chat_id, f'Извините, город {self.city} отсутствует в моей базе данных'
                + '\nили вы неправильно ввели название города☹'
                )

        if search_users(db, user_id = self.user_id) == True:

            schedule.every().day.at(take_user_time(db, user_id = self.user_id)).do(daily_forecast)

            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            pass
    

    def func_weather(self):
        @self.bot.message_handler(commands=['weather'] ,content_types=['text'])
        def input_data(message):
                user_city = self.bot.send_message(message.chat.id, 'Напишите интересующий вас город...')
                self.bot.register_next_step_handler(user_city, checking_weather)

        def checking_weather(message):

            self.city = message.text
            try:
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = pyowm.OWM(weather_api, config_dict)
                                        
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(self.city)
                w = observation.weather

                        #погодные характеристики
                pressure = str(w.pressure['press'] * 0.75) + ' мм.рт.ст'
                weather_now = w.detailed_status
                temp = str(w.temperature('celsius')['temp']) + '°C'
                max_temp = str(w.temperature('celsius')['temp_max']) + '°C'
                min_temp = str(w.temperature('celsius')['temp_min']) + '°C'
                temp_feels = str(w.temperature('celsius')['feels_like']) + '°C'
                wind = str(w.wind()['speed']) + ' м/с'
                humid = str(w.humidity) + ' %'

                self.bot.send_message(message.chat.id,

                f'🌤В городе {self.city} сейчас {weather_now}'
                + f'\n🌡Температура воздуха: {temp}'
                + f'\n🌡[max]Максимальная температура воздуха: {max_temp}'
                + f'\n🌡[min]Минимальная температура воздуха: {min_temp}'
                + f'\n🌡[+-]Ощущается: {temp_feels}'
                + f'\n\n💨Скорость ветра: {wind}'
                + f'\n💧Влажность: {humid}'
                + f'\n🌀Атмосферное давление: {pressure}'
                )

            except:
                self.bot.send_message(message.chat.id, f'Извините, город {self.city} отсутствует в моей базе данных'
                + '\nили вы неправильно ввели название города☹'
                )


if __name__ == '__main__':

    bot = telebot.TeleBot(TG_token)

    main = Weather_bot(bot)
    
    bot.polling(none_stop = True, interval = 0)