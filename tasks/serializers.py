from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, TaskAttachments, Tag
from bleach import clean

User = get_user_model()

allowed_tags = ["p", "br", "strong", "h1", "h2", "em", "b", "i", "u", "ul", "ol", "li"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    assigned_to_user = UserSerializer(source="assigned_to", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def validate_description(self, value):
        return clean(value, tags=allowed_tags)

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachments
        fields = ["id", "file", "uploaded_at"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
