# 시도 2
import os
import django
import requests
import json
from django.conf import settings

# Django 설정 초기화
# 초기화 미시행시, Django 설정(settings.py)을 사용할 때, DJANGO_SETTINGS_MODULE 환경 변수가 설정되지 않아서 오류 발생
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_pjt.settings")  # "your_project"를 실제 프로젝트 이름으로 변경
django.setup()

API_KEY = settings.TMDB_API_KEY
BASE_URL = 'https://api.themoviedb.org/3'
LAST_PAGE = 30    # TMDB API의 한 페이지에 포함된 데이터: 기본적으로 20개의 항목(4페이지라면 20*4)

# TMDB API 요청 함수
# def response_data(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"API 요청 실패: {url}, 상태 코드: {response.status_code}")
#         return {}

import time
# API 요청 함수 수정
def response_data(url):
    response = requests.get(url)
    if response.status_code == 429:  # Too Many Requests
        time.sleep(10)  # 10초 대기
        return response_data(url)  # 재시도
    return response.json()


# json 데이터 저장
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{filename} 생성")

# -------------------------------------------------------------------------------

# 한영 구분 배우정보 가져오기
def fetch_credits():
    actors_data = []

    # 한국 영화 데이터 요청
    for PAGE in range(1, LAST_PAGE + 1):
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&region=KR&page={PAGE}'
        data = response_data(url)

        for movie in data.get('results', []):
            movie_id = movie['id']
            credits_url = f'{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=ko-KR'
            credits_data = response_data(credits_url)

            for cast in credits_data.get('cast', []):
                if cast['id'] not in [actor['pk'] for actor in actors_data]:
                    actors_data.append({
                        "model": "movies.Actor",
                        "pk": cast['id'],
                        "fields": {
                            "name": cast['name'],
                            "profile_path": cast.get('profile_path', ''),
                            "language": "ko-KR"
                        }
                    })

    # 영어 데이터 요청 (전 세계 인기 영화)
    for PAGE in range(1, LAST_PAGE + 1):
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={PAGE}'
        data = response_data(url)

        for movie in data.get('results', []):
            movie_id = movie['id']
            credits_url = f'{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US'
            credits_data = response_data(credits_url)

            for cast in credits_data.get('cast', []):
                if cast['id'] not in [actor['pk'] for actor in actors_data]:
                    actors_data.append({
                        "model": "movies.Actor",
                        "pk": cast['id'],
                        "fields": {
                            "name": cast['name'],
                            "profile_path": cast.get('profile_path', ''),
                            "language": "en-US"
                        }
                    })

    save_to_json(actors_data, 'actors.json')



# 실행
fetch_credits()        # 배우 및 감독 데이터 저장

# --------------------------------------------------------------
# 랜덤으로 배우 정보 추출
# 한국 배우와 외국 배우 랜덤 추출
import random

def get_random_actors():
    with open('actors.json', 'r', encoding='utf-8') as f:
        actors_data = json.load(f)

    korean_actors = [actor for actor in actors_data if actor['fields']['language'] == "ko-KR"]
    foreign_actors = [actor for actor in actors_data if actor['fields']['language'] == "en-US"]

    # 한국 배우 25명, 외국 배우 25명 랜덤 추출(random.sample: 중복없이 원하는 개수 만큼 랜덤하게 선택)
    # 리스트 덧셈
    random_actors = random.sample(korean_actors, min(25, len(korean_actors))) + \
                    random.sample(foreign_actors, min(25, len(foreign_actors)))
    save_to_json(random_actors, 'random_actors.json')


# 입력된 이름이 한국어 이름인지 판별(language필드 사용시 없어도 됨)
# 입력된 문자열의 각 문자 순회, 유니코드 범위 사용해 문자가 한글인지 확인
# any(): 문자열에 한글이 하나라도 포함되어 있으면 True, 전혀 없으면 False
# def is_korean_name(name):
#     return any("\uac00" <= char <= "\ud7a3" for char in name)


# 배우 프로필 이미지 다운로드
def download_actor_images():
    with open('random_actors.json', 'r', encoding='utf-8') as f:
        actors = json.load(f)

    os.makedirs('actor_images2', exist_ok=True) # 디렉토리 생성(exist_ok=True: 디렏토리가 이미 있어도 오류 무시하고 넘어감)

    for actor in actors:
        profile_path = actor['fields']['profile_path']
        if profile_path:
            img_url = f"https://image.tmdb.org/t/p/w500{profile_path}"
            img_data = requests.get(img_url).content    # .content: 이미지(바이너리) 데이터 반환
            with open(f"actor_images2/{actor['fields']['name']}.jpg", "wb") as img_file: # 이미지 저장할 파일 열기
                img_file.write(img_data)    # 가져온 바이너리 데이터를 해당 파일에 저장
                print(f"{actor['fields']['name']} 이미지 다운로드 완료")


get_random_actors()
download_actor_images()

