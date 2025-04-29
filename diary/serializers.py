from korean_lunar_calendar import KoreanLunarCalendar
from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['date', 'lunar_date', 'content', 'weather']
        read_only_fields = ['lunar_date']

    def create(self, validated_data):
        date = validated_data.get('date')
        lunar_date = self.get_lunar_date(date)

        diary = Diary.objects.create(
            user=self.context['request'].user,
            date=date,
            lunar_date=lunar_date,
            content=validated_data.get('content'),
            weather=validated_data.get('weather')
        )
        return diary

    def update(self, instance, validated_data):
        date = validated_data.get('date', instance.date)
        lunar_date = self.get_lunar_date(date)

        instance.date = date
        instance.lunar_date = lunar_date
        instance.content = validated_data.get('content', instance.content)
        instance.weather = validated_data.get('weather', instance.weather)

        instance.save()
        return instance

    def get_lunar_date(self, date):
        calendar = KoreanLunarCalendar()
        calendar.setSolarDate(date.year, date.month, date.day)
        return f"{calendar.lunarYear}-{calendar.lunarMonth:02d}-{calendar.lunarDay:02d}"