from django.urls import path
from .views import DiaryCreateView, DiaryListView, DiaryDetailView, DiaryExportExcelView

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name='diary-create'),
    path('search/', DiaryListView.as_view(), name='diary-list'),  
    path('search/<int:pk>/', DiaryDetailView.as_view(), name='diary-detail'), 
    path('export/', DiaryExportExcelView.as_view(), name='diary-export'), 

]