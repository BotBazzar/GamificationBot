from django.urls import path
from application.views import *
urlpatterns = [
    path('app/users/', GetUsersInfoView.as_view()),
    #    path('admin/', admin.site.urls),
]
