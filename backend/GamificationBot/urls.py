from django.urls import path
from application.views import *
from bot.views import WebhookView

urlpatterns = [
    path('app/users/', GetUsersInfoView.as_view()),
    path('app/leaderboard/', GetLeaderboardView.as_view()),
    path('app/prizes/', GetPrizesView.as_view()),
    path('app/mark-spun/', GetPrizesView.as_view()),
    path('telegram/webhook/', WebhookView.as_view(), name='telegram_webhook'),
    #    path('admin/', admin.site.urls),
]
