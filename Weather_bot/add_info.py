from configure import MONGODB_LINK, MONGODB, TG_token
#from telegram_bot import daily_forecast

from pymongo import MongoClient

db = MongoClient(MONGODB_LINK)[MONGODB]

def search_users(db, user_id):
    user = db['users'].find_one({'user_id': user_id})
    if not user:
        return False

    elif user:
        return True

def save_users(db, user_id, time, city):
    db['users'].insert_one(
        {
        'user_id': user_id,
        'time': time,
        'city': city
    }
        )

def emailing_messages(db, city, time):
    pass

def take_user_time(db, user_id):
    user = db['users'].find_one({'user_id': user_id})['time']
    return user


def unsubscribe(db, user_id):
    user = db['users'].find_one({'user_id': user_id})

    if not user:
        return 'Вы не подписаны на рассылку'

    elif user:
        db['users'].remove({'user_id': user_id})
        return 'Вы успешно отписались от рассылки!'

