from rest_framework import serializers
#from .models import Account
from django.contrib.auth.models import User
from .models import Role

""" class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'display_name', 'bio', 'email'] """

class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "isAdmin"]

    def get_isAdmin(self, obj):
        return obj.roles.filter(name__iexact=Role.ADMIN).exists()