from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from tasks.views import TaskViewSet, TaskAttachmentViewSet, TagViewSet

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task")
attachments_router = routers.NestedSimpleRouter(router, r"", lookup="task")
attachments_router.register(r"attachments", TaskAttachmentViewSet, basename="task-attachments")

tag_router = DefaultRouter()
tag_router.register(r"", TagViewSet, basename="tag")

urlpatterns = [
    path("tasks/", include(router.urls)),
    path("tasks/", include(attachments_router.urls)),
    path("tags/", include(tag_router.urls)),
]

