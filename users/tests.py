from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class UserTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "ham1234!",
            "password2": "ham1234!",
            "nickname": "햄스터"
        }
        self.login_data = {
            "username": "testuser",
            "password": "ham1234!"
        }

    # 회원가입 테스트
    def test_user_register_success(self):
        response = self.client.post(reverse("register"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    # 회원가입 실패 테스트 (비밀번호 불일치)
    def test_user_register_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "wrongpass"
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    # 로그인 성공 테스트
    def test_login_success(self):
        self.client.post(reverse("register"), self.user_data)
        response = self.client.post(reverse("login"), self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data) # 응답에 access 토큰 있어야 정상이란뜻

    # 로그인 실패 테스트 (비번 틀림)
    def test_login_fail_wrong_password(self):
        self.client.post(reverse("register"), self.user_data)
        wrong_login = self.login_data.copy()
        wrong_login["password"] = "wrong1234"
        response = self.client.post(reverse("login"), wrong_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 유저 정보 GET (로그인 후)
    def test_user_info_me_get(self):
        self.client.post(reverse("register"), self.user_data)
        login_res = self.client.post(reverse("login"), self.login_data)
        token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.get(reverse("user-me"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "testuser")

    # 유저 정보 PATCH (닉네임 수정)
    def test_user_info_patch(self):
        self.client.post(reverse("register"), self.user_data)
        login_res = self.client.post(reverse("login"), self.login_data)
        token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        patch_data = {"nickname": "변경된햄"}
        res = self.client.patch(reverse("user-me"), patch_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["nickname"], "변경된햄")