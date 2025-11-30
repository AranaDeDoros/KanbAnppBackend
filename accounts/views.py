from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Return the currently authenticated user's info.
    """
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users(request):
    user_list = User.objects.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email}
                  for user in user_list]
    return Response(users_data)
