from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Return the currently authenticated user's info.
    """
    user = request.user
    return Response(UserSerializer(user).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users(request):
    queryset = User.objects.all()
    return Response(UserSerializer(queryset, many=True).data)
