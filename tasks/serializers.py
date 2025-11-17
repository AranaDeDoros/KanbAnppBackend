from rest_framework import serializers
from .models import Task
from bleach import clean

allowed_tags = ["p", "br", "strong", "h1", "h2", "em", "b", "i", "u", "ul", "ol", "li"]

class TaskSerializer(serializers.ModelSerializer):
    def validate_description(self, value):
        return clean(value, tags=allowed_tags)
    class Meta:
        model = Task
        fields = '__all__'
