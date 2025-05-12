# users/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# CreateAPIView 상속, 딱 POST요청만 처리함 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] 
    
# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
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
    
# 회원 정보 수정
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)