from django.contrib import admin
from .models import Diary

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'lunar_date', 'weather', 'created_at')
    search_fields = ('user__username', 'date', 'lunar_date', 'weather')
    list_filter = ('weather', 'date')
    ordering = ('-created_at',)