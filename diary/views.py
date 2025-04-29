from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework import generics, permissions
from .models import Diary
from .serializers import DiarySerializer

# POST, 다이어리 작성
class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사람만 작성 가능
    
# GET, 다이어리 조회+필터
class DiaryListView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Diary.objects.filter(user=user).order_by('-date')  # 기본: 최신순

        # 쿼리파라미터 받기
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        keyword = self.request.query_params.get('keyword')

        # 날짜 필터링
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        # 키워드 검색
        if keyword:
            queryset = queryset.filter(content__icontains=keyword)

        return queryset
    
# 글 상세 조회, 수정, 삭제
class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Diary.objects.filter(user=user)

# 글 내보내기
class DiaryExportExcelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        diaries = Diary.objects.filter(user=user).order_by('-date')

        wb = Workbook()
        ws = wb.active
        ws.title = "Diaries"

        # 엑셀 첫 번째 줄 (헤더)
        ws.append(["날짜 (양력)", "날짜 (음력)", "내용", "날씨"])

        # 데이터 추가
        for diary in diaries:
            ws.append([
                diary.date.strftime("%Y-%m-%d"),
                diary.lunar_date,
                diary.content,
                diary.weather,
            ])

        # 엑셀 파일 응답
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=diary_export.xlsx'
        wb.save(response)

        return response