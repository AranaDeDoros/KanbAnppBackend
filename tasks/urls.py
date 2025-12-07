from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from tasks.views import TaskViewSet, TaskAttachmentViewSet

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task")

attachments_router = routers.NestedSimpleRouter(router, r"", lookup="task")
attachments_router.register(r"attachments", TaskAttachmentViewSet, basename="task-attachments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(attachments_router.urls)),
]

