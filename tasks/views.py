from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, TaskAttachments
from .serializers import TaskSerializer, TaskAttachmentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset


    def create(self, request, *args, **kwargs):
        attachments = request.FILES.getlist("file_attachments")

        if not self.__validate_attachments__(attachments):
            return Response(
                {"error": "You can upload a maximum of 5 attachments per task."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        for file in attachments:
            TaskAttachments.objects.create(task=task, file=file)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        attachments = request.FILES.getlist("file_attachments")

        if not self.__validate_attachments__(attachments):
            return Response(
                {"error": "You can upload a maximum of 5 attachments per task."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = super().partial_update(request, *args, **kwargs)

        task = self.get_object()

        for file in attachments:
            TaskAttachments.objects.create(task=task, file=file)

        return response

    def __validate_attachments__(self, attachments) -> bool:
        if len(attachments) > 5:
           return False
        return True


#wip
class TaskAttachmentViewSet(viewsets.ViewSet):

    def list(self, request, task_pk=None):
        task = get_object_or_404(Task, pk=task_pk)
        attachments = task.attachments.all()
        serializer = TaskAttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    def create(self, request, task_pk=None):
        task = get_object_or_404(Task, pk=task_pk)

        files = request.FILES.getlist("file_attachments")

        created_items = []
        for f in files:
            attach = TaskAttachments.objects.create(task=task, file=f)
            created_items.append(attach)

        serializer = TaskAttachmentSerializer(created_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, task_pk=None):
        task = get_object_or_404(Task, pk=task_pk)
        attachment = get_object_or_404(TaskAttachments, pk=pk, task=task)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
