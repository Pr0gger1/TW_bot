from Configs.configure import MONGODB_LINK, db_collection

from pymongo import MongoClient

db = MongoClient(MONGODB_LINK)[db_collection]


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
    return 'Ваши данные успешно сохранены!'


def modify_data(db, user_id, time, city):
    pass


def remove_users(db, user_id):
    user = db['users'].find_one({'user_id': user_id})

    if not user:
        return 'Вы не подписаны на рассылку'

    db['users'].remove({'user_id': user_id})
    return 'Вы успешно отписались от рассылки!'


take_user_time = lambda db, user_id: db['users'].find_one({'user_id': user_id})['time']

take_user_city = lambda db, user_id: db['users'].find_one({'user_id': user_id})['city']

