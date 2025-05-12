import requests
import datetime
from django.conf import settings
from urllib.parse import urlencode

# 좌표
NX = 60
NY = 137

SERVICE_KEY = settings.WEATHER_API_KEY 

BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"



def get_base_datetime():
    """단기예보용 base_date, base_time 생성"""
    now = datetime.datetime.now()
    hour = now.hour
    base_times = [2, 5, 8, 11, 14, 17, 20, 23]

    candidate_times = [t for t in base_times if t <= hour]
    if candidate_times:
        closest_time = max(candidate_times)
        base_date = now.strftime('%Y%m%d')
    else:
        # 새벽 0~1시면 어제 날짜로 잡고 마지막 시간(23시) 사용
        closest_time = base_times[-1]
        base_date = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')

    base_time = f"{closest_time:02d}00"
    return base_date, base_time

def get_current_base_datetime():
    """초단기실황용 base_date, base_time 생성"""
    now = datetime.datetime.now()
    base_date = now.strftime('%Y%m%d')

    # 정시 기준으로 한 시간 전 (10:10분이면 base_time=1000)
    base_time = now.strftime('%H') + "00"

    return base_date, base_time





def fetch_weather_forecast(target_date=None, force_time=None):
    if target_date is None:
        target_date = get_base_datetime()[0] 

    base_date, base_time = get_base_datetime()

    query_params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": NX,
        "ny": NY
    }

    url = f"{BASE_URL}/getVilageFcst?{urlencode(query_params)}"

    try:
        response = requests.get(url)
        data = response.json()

        # 추출할 category
        target_cats = ['POP', 'PTY', 'SKY', 'TMN', 'TMX']
        result = {}

        for cat in target_cats:
            for item in data['response']['body']['items']['item']:
                if item['category'] == cat and item['fcstDate'] == target_date:
                    # 최신 항목으로 업데이트 
                    result[cat] = item['fcstValue']
        return result

    except Exception as e:
        print("날씨 API 호출 실패:", e)
        return {"error": str(e)}
    
def fetch_weather_now():
    base_date, base_time = get_current_base_datetime()

    query_params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": NX,
        "ny": NY
    }

    url = f"{BASE_URL}/getUltraSrtNcst?{urlencode(query_params)}"

    try:
        response = requests.get(url)
        print("🔍 [실황] 응답 코드:", response.status_code)
        data = response.json()

        # 추출할 항목: T1H (기온), REH (습도), PTY (강수형태)
        target_cats = ['T1H', 'REH', 'PTY']
        result = {cat: None for cat in target_cats}

        for item in data['response']['body']['items']['item']:
            if item['category'] in target_cats:
                # 최신 정보로 업뎃되게
                result[item['category']] = item['obsrValue']

        return result

    except Exception as e:
        print("실황 날씨 API 호출 실패:", e)
        return {"error": str(e)}