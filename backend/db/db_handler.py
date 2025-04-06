from db.models import *


def add_new_user(chat_id, username, first_name, last_name):
    u = User(chat_id=chat_id, username=username, first_name=first_name, last_name=last_name)
    u.save()
    User.assign_prize(u)


def user_exists(chat_id):
    print(chat_id)
    return User.objects.filter(chat_id=chat_id).exists()

def update_user_score(chat_id, score):
    user = User.objects.get(chat_id=chat_id)
    user.score += score
    user.answers += 1
    user.save()