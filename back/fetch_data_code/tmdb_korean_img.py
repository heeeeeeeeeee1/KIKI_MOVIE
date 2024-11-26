import requests
import os
from django.conf import settings

# API_KEY = os.getenv("TMDB_API_KEY") 
API_KEY = "settings.TMDB_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
actors = [
    "강동원", "강소라", "강하늘", "고아성", "고현정", "공효진", "김고은", "김남길",
    "김민희", "김수현", "김태리", "김혜수", "남주혁", "류준열", "마동석", "박보영",
    "박서준", "박신혜", "박해일", "배두나", "배수지", "변요한", "손예진", "송강호",
    "송중기", "신민아", "안성기", "유아인", "유연석", "이병헌", "이정재", "이종석",
    "이주연", "임시완", "전도연", "전지현", "정우성", "조인성", "주지훈", "지창욱",
    "차승원", "최민식", "한지민", "한효주", "황정민", "현빈", "김윤석", "김희애",
    "이성민", "조진웅"
]

output_folder = "actor_images"
os.makedirs(output_folder, exist_ok=True)

def download_actor_images(actor_list):
    for actor in actor_list:
        try:
            search_url = f"{BASE_URL}/search/person"
            params = {"api_key": API_KEY, "query": actor, "language": "ko"}
            response = requests.get(search_url, params=params)

            # 응답 상태 코드 확인
            if response.status_code != 200:
                print(f"Failed to fetch data for {actor}. Status code: {response.status_code}")
                continue

            data = response.json()

            # 응답 데이터 구조 확인
            if 'results' not in data:
                print(f"'results' key not found in response for {actor}. Response: {data}")
                continue

            if not data['results']:
                print(f"No results found for {actor}.")
                continue

            actor_info = data['results'][0]
            profile_path = actor_info.get("profile_path")

            if profile_path:
                image_url = f"{IMAGE_BASE_URL}{profile_path}"
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    file_name = f"{actor}.jpg"
                    file_path = os.path.join(output_folder, file_name)
                    with open(file_path, "wb") as img_file:
                        img_file.write(image_response.content)
                    print(f"Downloaded: {actor} -> {file_name}")
                else:
                    print(f"Failed to download image for {actor}")
            else:
                print(f"No image found for {actor}")
        except Exception as e:
            print(f"An error occurred for {actor}: {e}")

# 실행
download_actor_images(actors)
