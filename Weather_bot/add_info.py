from configure import MONGODB_LINK, MONGODB, TG_token

from pymongo import MongoClient

db = MongoClient(MONGODB_LINK)[MONGODB]


def save_searh_users(db, user_id, time, city):
    user = db['users'].find_one({'user_id': user_id})
    if not user:
        user = {
            'user_id': user_id,
            'city': city,
            'time': time
        }
        db['users'].insert_one(user)



def emailing_messages(db, city, time):
    pass

def take_user(db, user_id):
    user = db['users'].find_one({'user_id': user_id})['time']
    return user


def unsubscribe(db, user_id):
    db['users'].remove({'user_id': user_id})

