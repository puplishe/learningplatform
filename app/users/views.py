from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action


from .serializers import UserSerializer

from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            
            token, created = Token.objects.get_or_create(user=user)

            
            response_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,  
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
