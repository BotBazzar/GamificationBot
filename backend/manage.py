#!/usr/bin/env python
import os
import sys

from GamificationBot.settings import ALLOWED_HOSTS

# !/usr/bin/env python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def init_django():
    import django
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        DEFAULT_AUTO_FIELD='django.db.models.AutoField'
        ,
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': f'{BASE_DIR}/db.sqlite3',
            }
        }, DEBUG=False,ALLOWED_HOSTS=['*']
        # DATABASES={
        #     'default': {
        #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #         'NAME': 'tousradieh',
        #         'USER': 'postgres',
        #         'PASSWORD': 'postgres',
        #         'HOST': 'localhost',
        #         'PORT': '5432',
        #     }
        # }
    )
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    # init_django()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GamificationBot.settings')
    execute_from_command_line(sys.argv)
