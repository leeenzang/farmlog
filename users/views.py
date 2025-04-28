# users/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from .models import User
from .serializers import RegisterSerializer, LoginSerializer

# CreateAPIView 상속, 딱 POST요청만 처리함 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer
    
# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'nickname': user.nickname,
        }, status=status.HTTP_200_OK)

# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사람만 로그아웃 가능

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)