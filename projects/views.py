from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from accounts.models import IsAdminRole

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        admin_actions = ["create", "update", "partial_update", "destroy"]
        if self.action in admin_actions:
            return [IsAuthenticated(), IsAdminRole()]
        #view okay for regulars
        return [IsAuthenticated()]