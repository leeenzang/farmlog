from django.urls import path
from users.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # 회원가입
    path("login/", LoginView.as_view(), name="login"),            # 로그인
    path("logout/", LogoutView.as_view(), name="logout"),         # 로그아웃
]