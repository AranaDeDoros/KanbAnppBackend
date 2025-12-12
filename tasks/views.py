from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, TaskAttachments, Tag
from .serializers import TaskSerializer, TaskAttachmentSerializer, TagSerializer
from rest_framework.decorators import action
from rest_framework import status

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset


    def create(self, request, *args, **kwargs):
        attachments = request.FILES.getlist("attachments")


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

        for tag_id in request.data.get("tags", []):
            tag = get_object_or_404(Tag, id=tag_id)
            task.tags.add(tag)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        attachments = request.FILES.getlist("attachments")

        if not self.__validate_attachments__(attachments):
            return Response(
                {"error": "You can upload a maximum of 5 attachments per task."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = super().partial_update(request, *args, **kwargs)

        task = self.get_object()

        for file in attachments:
            TaskAttachments.objects.create(task=task, file=file)

        for tag_id in request.data.get("tags", []):
            tag = get_object_or_404(Tag, id=tag_id)
            task.tags.add(tag)

        return response

    def __validate_attachments__(self, attachments) -> bool:
        if len(attachments) > 5:
           return False
        return True


class TaskAttachmentViewSet(viewsets.ViewSet):

    def list(self, request, task_pk=None):
        task = get_object_or_404(Task, pk=task_pk)
        attachments = task.attachments.all()
        serializer = TaskAttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    def create(self, request, task_pk=None):
        task = get_object_or_404(Task, pk=task_pk)

        files = request.FILES.getlist("attachments")

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



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all()
        names = self.request.query_params.getlist("name", [])

        # name=a,b,c
        if len(names) == 1 and "," in names[0]:
            names = names[0].split(",")

        if names:
            queryset = queryset.filter(name__in=[n.lower() for n in names])

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search.lower())

        return queryset

    @action(detail=False, methods=["post","put"], url_path="bulk")
    def bulk_create(self, request):
        tags = request.data.get("newTags", [])

        if not isinstance(tags, list):
            return Response({"error": "tags must be a list"}, status=400)

        normalized = [t.strip().lower() for t in tags if t.strip()]
        normalized = list(set(normalized))  # dupes removal

        created = []

        for name in normalized:
            tag, was_created = Tag.objects.get_or_create(name=name)
            if was_created:
                created.append(tag)


        serializer = TagSerializer(created , many=True)
        return Response(
            {
                "created": TagSerializer(created, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="autocomplete")
    def autocomplete(self, request):
        query = request.query_params.get("query")

        if not query:
            return Response([], status=200)

        results = Tag.objects.filter(name__icontains=query.lower())[:10]

        serializer = TagSerializer(results, many=True)
        return Response(serializer.data)