from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    The 'owner' field is set as read-only to prevent changes via API requests,
    ensuring that ownership can only be set internally.
    """
    owner = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ["owner"]
