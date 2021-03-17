from telebot import types

inline_info_key = types.InlineKeyboardMarkup()
inline_info_btn_oprties = types.InlineKeyboardButton(text='Что ты умеешь?',
                                                     callback_data='about_bot')

inline_info_btn_guide = types.InlineKeyboardButton(text='Запрос погоды?',
                                                   callback_data='get_weather')

inline_info_key.add(inline_info_btn_guide, inline_info_btn_oprties)
