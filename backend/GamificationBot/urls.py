from django.urls import path
from application.views import *
from bot.views import telegram_webhook
urlpatterns = [
    path('app/users/', GetUsersInfoView.as_view()),
    path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    #    path('admin/', admin.site.urls),
]
