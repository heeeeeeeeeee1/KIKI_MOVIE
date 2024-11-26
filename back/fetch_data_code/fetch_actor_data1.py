#  데이터 수집을 위한 여러 시도 중 하나... 한국 배우 25명, 외국 배우 25명 랜덤으로 
import os
import json
import random
import requests
import time
from django.conf import settings

# Django 설정 초기화
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_pjt.settings")
import django
django.setup()

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"
LAST_PAGE = 20  # 최대 페이지 설정


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


# 1. 글로벌 배우 데이터 가져오기
def fetch_global_actors():
    actors_data = []
    for PAGE in range(1, LAST_PAGE + 1):
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
                        "language": "en-US"
                    }
                })
    save_to_json(actors_data, "global_actors.json")


# 2. 한국 배우 데이터 가져오기
def fetch_korean_movie_actors():
    actors_data = []
    for PAGE in range(1, LAST_PAGE + 1):
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&region=KR&page={PAGE}"
        data = response_data(url)

        for movie in data.get("results", []):
            movie_id = movie["id"]
            credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=ko-KR"
            credits_data = response_data(credits_url)

            for cast in credits_data.get("cast", []):
                if cast["id"] not in [actor["pk"] for actor in actors_data]:
                    actors_data.append({
                        "model": "movies.Actor",
                        "pk": cast["id"],
                        "fields": {
                            "name": cast["name"],
                            "profile_path": cast.get("profile_path", ""),
                            "language": "ko-KR"
                        }
                    })
    save_to_json(actors_data, "korean_actors.json")


# 3. 글로벌 배우와 한국 배우 데이터 병합
def merge_korean_and_global_actors():
    with open("global_actors.json", "r", encoding="utf-8") as global_file:
        global_actors = json.load(global_file)
    with open("korean_actors.json", "r", encoding="utf-8") as korean_file:
        korean_actors = json.load(korean_file)

    all_actors = global_actors + korean_actors
    save_to_json(all_actors, "merged_actors.json")


# 4. 랜덤으로 배우 50명 추출 (한국 배우 25명, 외국 배우 25명)
def get_random_actors_from_merged():
    with open("merged_actors.json", "r", encoding="utf-8") as f:
        actors_data = json.load(f)

    korean_actors = [actor for actor in actors_data if actor["fields"]["language"] == "ko-KR"]
    foreign_actors = [actor for actor in actors_data if actor["fields"]["language"] == "en-US"]

    random_korean_actors = random.sample(korean_actors, min(25, len(korean_actors)))
    random_foreign_actors = random.sample(foreign_actors, min(25, len(foreign_actors)))

    random_actors = random_korean_actors + random_foreign_actors
    save_to_json(random_actors, "random_actors.json")


# 5. 랜덤 추출된 배우의 이미지 다운로드
def download_actor_images():
    with open("random_actors.json", "r", encoding="utf-8") as f:
        actors = json.load(f)

    os.makedirs("actor_images3", exist_ok=True)

    for actor in actors:
        profile_path = actor["fields"]["profile_path"]
        if profile_path:
            img_url = f"https://image.tmdb.org/t/p/w500{profile_path}"
            try:
                img_data = requests.get(img_url).content
                safe_name = actor["fields"]["name"].replace(" ", "_").replace("/", "_")
                with open(f"actor_images3/{safe_name}.jpg", "wb") as img_file:
                    img_file.write(img_data)
                    print(f"{actor['fields']['name']} 이미지 다운로드 완료")
            except Exception as e:
                print(f"{actor['fields']['name']} 이미지 다운로드 실패: {e}")


# 전체 실행
fetch_global_actors()             # 글로벌 배우 데이터 가져오기
fetch_korean_movie_actors()       # 한국 배우 데이터 가져오기
merge_korean_and_global_actors()  # 글로벌 배우와 한국 배우 데이터 병합
get_random_actors_from_merged()   # 랜덤으로 배우 50명 추출
download_actor_images()           # 배우 이미지 다운로드
