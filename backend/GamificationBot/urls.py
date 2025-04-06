from django.urls import path
from application.views import *
from bot.views import telegram_webhook
urlpatterns = [
    path('app/users/', GetUsersInfoView.as_view()),
    path('app/leaderboard/', GetLeaderboardView.as_view()),
    path('app/prizes/', GetPrizesView.as_view()),
    path('app/mark-spun/', GetPrizesView.as_view()),
    path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    #    path('admin/', admin.site.urls),
]
