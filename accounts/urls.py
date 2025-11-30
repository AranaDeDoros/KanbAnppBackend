# urls.py
from django.urls import path
from .views import current_user, users

urlpatterns = [
    path('me/', current_user, name='current_user'),
    path('users/', users, name='users'),
]
