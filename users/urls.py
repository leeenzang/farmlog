from django.urls import path
from users.views import RegisterView, LoginView, LogoutView,UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # 회원가입
    path("login/", LoginView.as_view(), name="login"),            # 로그인
    path("logout/", LogoutView.as_view(), name="logout"),         # 로그아웃
    path("me/", UserMeView.as_view(), name="user-me"),          # 회원정보 수정

]