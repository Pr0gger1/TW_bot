from telebot import types

key_forecast = types.ReplyKeyboardMarkup(resize_keyboard = True)
key_sub_btn = types.KeyboardButton(text = 'Подписаться на рассылку погоды')
key_unsub_btn = types.KeyboardButton(text = 'Отписаться от рассылки погоды')
key_forecast.row(key_sub_btn, key_unsub_btn)