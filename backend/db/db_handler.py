from db.models import *


def add_new_user(full_name, chat_id, employee_id):
    u = User(chat_id=chat_id)
    u.save()
    e = Employee(full_name=full_name, employee_id=employee_id, user=u)
    e.save()


def user_exists(chat_id):
    print(chat_id)
    u = User.objects.filter(chat_id=chat_id)
    if len(u) == 0:
        return False
    return True


def user_is_leader(chat_id):
    return False
