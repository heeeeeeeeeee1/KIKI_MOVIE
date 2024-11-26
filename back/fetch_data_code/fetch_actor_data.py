# 결국 인기배우 상위 50명에 대한 정보 가져옴
import os
import json
import requests
import time
from django.conf import settings

# Django 설정 초기화
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_pjt.settings")
import django
django.setup()

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"


# TMDB API 요청 함수
def response_data(url):
    response = requests.get(url)
    if response.status_code == 429:  # Too Many Requests
        print("요청 제한 도달. 10초 대기 후 재시도...")
        time.sleep(10)
        return response_data(url)  # 재시도
    if response.status_code != 200:
        print(f"API 요청 실패: {url}, 상태 코드: {response.status_code}")
        return {}
    return response.json()


# JSON 데이터 저장 함수
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{filename} 생성 완료")


# 1. TMDB에서 가장 인기 있는 배우 50명 가져오기
def fetch_top_actors():
    actors_data = []
    # TMDB의 /person/popular 엔드포인트에서 첫 번째 3페이지 데이터 사용 (20명 * 3페이지 = 최대 60명)
    for PAGE in range(1, 4):  # 3페이지까지 가져오기
        url = f"{BASE_URL}/person/popular?api_key={API_KEY}&language=en-US&page={PAGE}"
        data = response_data(url)

        for person in data.get("results", []):
            if person["id"] not in [actor["pk"] for actor in actors_data]:
                actors_data.append({
                    "model": "movies.Actor",
                    "pk": person["id"],
                    "fields": {
                        "name": person["name"],
                        "profile_path": person.get("profile_path", ""),
                        "popularity": person.get("popularity", 0),
                        "known_for": [movie.get("title", "") or movie.get("name", "") for movie in person.get("known_for", [])]
                    }
                })

    # 상위 50명 추출 (중복 없이)
    actors_data = actors_data[:50]  # 상위 50명만 남김
    save_to_json(actors_data, "top_actors.json")


# 2. 배우 프로필 이미지 다운로드
def download_actor_images():
    with open("top_actors.json", "r", encoding="utf-8") as f:
        actors = json.load(f)

    os.makedirs("actor_images_real", exist_ok=True)

    for actor in actors:
        profile_path = actor["fields"]["profile_path"]
        if profile_path:
            img_url = f"https://image.tmdb.org/t/p/w500{profile_path}"
            try:
                img_data = requests.get(img_url).content
                safe_name = actor["fields"]["name"].replace(" ", "_").replace("/", "_")
                with open(f"actor_images_real/{safe_name}.jpg", "wb") as img_file:
                    img_file.write(img_data)
                    print(f"{actor['fields']['name']} 이미지 다운로드 완료")
            except Exception as e:
                print(f"{actor['fields']['name']} 이미지 다운로드 실패: {e}")


# 실행
fetch_top_actors()  # 가장 인기 있는 배우 50명 가져오기
download_actor_images()  # 배우 프로필 이미지 다운로드
