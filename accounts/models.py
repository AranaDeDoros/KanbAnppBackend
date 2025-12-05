from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        return self.name

from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Admin access only
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.roles.filter(name="Admin").exists()
