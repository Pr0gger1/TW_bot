# Import config modules
from Configs.configure import TG_token, weather_api
# Import module for working with database
from User_data import db_func

# Import modules for working with telegram bot
import telebot
from telebot import types
from Keyboards.fc_key import key_forecast
from Keyboards.inline_key import inline_info_key

from User_data.email_msg import loop


class Weather_bot:
    def __init__(self):
        self.command_handler()

    def get_user_id(self):
        @bot.message_handler()
        def init_msg(message):
            self.user_id = message.from_user.id

            return self.user_id

    # Handler for command "/start"
    def command_handler(self):

        @bot.message_handler(commands=['start'])
        def start(message):

            bot.send_message(message.chat.id,
                             f'Привет, {message.from_user.first_name},'
                             + 'я бот, призванный облегчить наблюдение за погодой😉.'
                             + '\nНапиши мне свой город и я расскажу, всё что знаю о нём.\nВведите команду /info, '
                               'если что-то непонятно))',
                             reply_markup=key_forecast)

        # Handler for command "/info"
        @bot.message_handler(commands=['info'])
        def info(message):

            bot.send_message(message.chat.id, 'Что вы хотите узнать обо мне?', reply_markup=inline_info_key)

        # Handler for command "/weather"
        @bot.message_handler(commands=['weather'])
        def weather(message):
            city_input = bot.send_message(message.chat.id, 'Введите интересующий вас город...')
            bot.register_next_step_handler(city_input, user_city)

        def user_city(message):
            from Weather.current_weather import get_curr_weather

            input_city = message.text

            bot.send_message(message.chat.id, get_curr_weather(input_city))

        # Handler for forecast keyboard
        @bot.message_handler(content_types=['text'])
        def forecast_commands(message):

            if message.text == 'Подписаться на рассылку погоды':
                check_subscribe = db_func.search_users(db_func.db, user_id=self.get_user_id())

                if not check_subscribe:
                    fc_data_msg = bot.send_message(message.chat.id, 'Город?')

                    bot.register_next_step_handler(fc_data_msg, input_fc_city)

                elif check_subscribe == True:
                    bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку')

            elif message.text == 'Отписаться от рассылки погоды':
                bot.send_message(message.chat.id, db_func.remove_users(db_func.db, user_id=self.get_user_id()))

        def input_fc_city(message):
            self.city = message.text

            fc_data_msg = bot.send_message(message.chat.id, 'Время (чч:мм)?')
            bot.register_next_step_handler(fc_data_msg, input_fc_time)

        def input_fc_time(message):
            time = message.text

            bot.send_message(message.chat.id, db_func.save_users(db_func.db, user_id=self.get_user_id(), time=time, city=self.city))
            loop(time)

        # Callback handler for inline button
        @bot.callback_query_handler(func=lambda call: True)
        def request_callback(call):
            if call.data == 'about_bot':

                bot.send_message(call.message.chat.id, 'Я могу узнать текущую погоду вашего города.'
                                                       'Всё просто, вы пишите мне свой город, а я обрабатываю запрос '
                                                       'с помощью Python и '
                                                       'его библиотеки '
                                                       'pyowm, получаю результат и отправляю его вам.😉 ')

            elif call.data == 'get_weather':
                bot.send_message(call.message.chat.id, 'Узнать погоду можно, вызвав команду /weather')

    '''def set_city(self, message):
        self.city = message.text

        time_input = bot.send_message(message.chat.id, 'Время отправки прогноза? (чч:мм)')
        bot.register_next_step_handler(time_input, self.set_time)

    def set_time(self, message):
        self.time = message.text

        self.save_sub()

    def save_sub(self):

        reg_user.save_users(reg_user.db, user_id=self.user_id, time=self.time, city=self.city)
        self.bot.send_message(self.user_id, 'Вы успешно подписались на рассылку!😎')

        self.send_forecast()'''

    '''def send_forecast(self):

        def daily_forecast():
            try:
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = pyowm.OWM(weather_api, config_dict)

                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(
                    reg_user.take_user_city(reg_user.db, user_id=self.user_id)
                )

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
                self.bot.send_message(self.message_chat_id,
                                      f'Извините, город {self.city} отсутствует в моей базе данных'
                                      + '\nили вы неправильно ввели название города☹'
                                      )

        if reg_user.search_users(reg_user.db, user_id=self.user_id) == True:

            schedule.every().day.at(reg_user.take_user_time(reg_user.db, user_id=self.user_id)).do(daily_forecast)

            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            pass'''


if __name__ == '__main__':
    bot = telebot.TeleBot(TG_token)

    main = Weather_bot()

    bot.polling(none_stop=True, interval=0)
