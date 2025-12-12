from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, TaskAttachments, Tag
from bleach import clean
import json

User = get_user_model()

allowed_tags = ["p", "br", "strong", "h1", "h2", "em", "b", "i", "u", "ul", "ol", "li"]


class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachments
        fields = ["id", "file", "uploaded_at"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

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
    tags = TagSerializer(many=True, required=False)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def validate_description(self, value):
        return clean(value, tags=allowed_tags)

    def create(self, validated_data):
        request = self.context.get("request")

        tags_existing_raw = request.data.get("existingTags", "[]")
        tags_existing = json.loads(tags_existing_raw)

        tags_new_raw = request.data.get("newTags", "[]")
        tags_new = json.loads(tags_new_raw)

        task = Task.objects.create(**validated_data)

        if tags_existing:
            task.tags.add(*tags_existing)

        for name in tags_new:
            tag, _ = Tag.objects.get_or_create(name=name.lower())
            task.tags.add(tag)

        for file in request.FILES.getlist("attachments"):
            TaskAttachments.objects.create(task=task, file=file)

        return task

    def update(self, instance, validated_data):
        request = self.context.get("request")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if "tags_existing" in request.data or "tags_new" in request.data:
            tags_existing = json.loads(request.data.get("tags_existing", "[]"))
            tags_new = json.loads(request.data.get("tags_new", "[]"))

            instance.tags.clear()

            if tags_existing:
                instance.tags.add(*tags_existing)

            for name in tags_new:
                tag, _ = Tag.objects.get_or_create(name=name.lower())
                instance.tags.add(tag)

        for file in request.FILES.getlist("attachments"):
            TaskAttachments.objects.create(task=instance, file=file)

        return instance

