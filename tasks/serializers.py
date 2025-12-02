from rest_framework import serializers
from .models import Task
from bleach import clean

allowed_tags = ["p", "br", "strong", "h1", "h2", "em", "b", "i", "u", "ul", "ol", "li"]


from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    def validate_description(self, value):
        return clean(value, tags=allowed_tags)
    class Meta:
        model = Task
        fields = '__all__'
