from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Role
from rest_framework_simplejwt.tokens import RefreshToken

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

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)

        # Assign admin role by default, dev only, for mvp
        collaborator_role, _ = Role.objects.get_or_create(name=Role.ADMIN)
        user.roles.add(collaborator_role)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        response_data = UserSerializer(user).data
        response_data['access'] = str(refresh.access_token)
        response_data['refresh'] = str(refresh)

        return Response(response_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

