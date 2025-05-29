from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Diary
from datetime import date

User = get_user_model()

class DiaryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', nickname='햄스터')
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_diary(self):
        url = reverse('diary-create')
        data = {
            "date": "2024-05-28",
            "content": "오늘 비 와서 모종 심기 힘들었음",
            "weather": "비"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Diary.objects.count(), 1)
        self.assertEqual(Diary.objects.first().content, "오늘 비 와서 모종 심기 힘들었음")

    def test_list_diaries(self):
        Diary.objects.create(
            user=self.user,
            date=date.today(),
            lunar_date="2024-04-20",
            content="씨 뿌림",
            weather="맑음"
        )
        url = reverse('diary-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_diary(self):
        diary = Diary.objects.create(
            user=self.user,
            date=date.today(),
            lunar_date="2024-04-20",
            content="기록 전",
            weather="흐림"
        )
        url = reverse('diary-detail', args=[diary.id])
        data = {
            "date": str(date.today()),
            "content": "기록 수정함",
            "weather": "맑음"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "기록 수정함")

    def test_delete_diary(self):
        diary = Diary.objects.create(
            user=self.user,
            date=date.today(),
            lunar_date="2024-04-20",
            content="삭제 예정",
            weather="흐림"
        )
        url = reverse('diary-detail', args=[diary.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Diary.objects.count(), 0)