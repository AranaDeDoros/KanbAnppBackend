# urls.py
from django.urls import path
from .views import current_user

urlpatterns = [
    path('me/', current_user, name='current_user'),
]
