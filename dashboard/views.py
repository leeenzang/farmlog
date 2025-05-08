
from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.weather_api import fetch_weather_forecast, fetch_weather_now
from datetime import datetime, timedelta

def determine_weather_status(pty_code: str, sky_code: str) -> str:
    if pty_code and pty_code != "0":
        pty_map = {
            "1": "비",
            "2": "비/눈",
            "3": "눈",
            "4": "소나기",
            "5": "빗방울",
            "6": "빗방울눈날림",
            "7": "눈날림",
        }
        return pty_map.get(pty_code, "강수")
    else:
        sky_map = {
            "1": "맑음",
            "3": "구름많음",
            "4": "흐림",
        }
        return sky_map.get(sky_code, "알 수 없음")
    
    
class WeatherTodayView(APIView):
    def get(self, request):
        now_data = fetch_weather_now()

        today = datetime.now().strftime('%Y%m%d')
        forecast_data = fetch_weather_forecast(target_date=today)

        pty = now_data.get("PTY")
        sky = forecast_data.get("SKY")

        weather_status = determine_weather_status(pty_code=pty, sky_code=sky)

        result = {
            "weatherStatus": weather_status,     # 비 or 흐림 or 맑음 등
            "temperature": now_data.get("T1H"),  # 현재 기온
            "humidity": now_data.get("REH")      # 현재 습도
        }

        return Response(result)
    

class WeatherTomorrowView(APIView):
    def get(self, request):
        # 내일 날짜 문자열 생성
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')

        # 내일 예보 호출
        forecast_data = fetch_weather_forecast(target_date=tomorrow_date)

        # 날씨 상태 결정 (PTY 우선, SKY 대체)
        weather_status = determine_weather_status(
            pty_code=forecast_data.get("PTY"),
            sky_code=forecast_data.get("SKY")
        )

        result = {
            "weatherStatus": weather_status,
            "precipitationType": forecast_data.get("PTY"),     # PTY 코드
            "precipitationProbability": forecast_data.get("POP"),  # 강수확률
            "lowestTemp": forecast_data.get("TMN"),
            "highestTemp": forecast_data.get("TMX")
        }

        return Response(result)