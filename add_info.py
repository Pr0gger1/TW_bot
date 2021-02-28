from configure import MONGODB_LINK, MONGODB, TG_token

from pymongo import MongoClient

db = MongoClient(MONGODB_LINK)[MONGODB]

def search_users(db, user_id):
    user = db['users'].find_one({'user_id': user_id})
    return bool(user)

def save_users(db, user_id, time, city):
    db['users'].insert_one(
        {
        'user_id': user_id,
        'time': time,
        'city': city
    }
        )

def modify_data(db, user_id, time, city):
    pass

def remove_users(db, user_id):
    user = db['users'].find_one({'user_id': user_id})

    if not user:
        return 'Вы не подписаны на рассылку'

    db['users'].remove({'user_id': user_id})
    return 'Вы успешно отписались от рассылки!'


def take_user_time(db, user_id):
    return db['users'].find_one({'user_id': user_id})['time']

def take_user_city(db, user_id):
    return db['users'].find_one({'user_id': user_id})['city']
