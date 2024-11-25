from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, UnidentifiedImageError
import os
import numpy as np
import tensorflow as tf
import json
import requests
from django.conf import settings

# BASE_DIR은 프로젝트의 루트 디렉토리입니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 모델 파일 경로와 라벨 파일 경로를 지정합니다.
MODEL_PATH = os.path.join(BASE_DIR, "apps", "predictions", "teachable_machine_model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "apps", "predictions", "teachable_machine_model", "labels")

# TMDB API 키를 설정합니다.
TMDB_API_KEY = "TMDB_API_KEY"  # 실제 TMDB API 키로 변경 필요


def get_actor_movies(actor_name):
    """
    TMDB API를 사용하여 배우 이름을 기반으로 출연작 정보를 가져옵니다.
    """
    # 배우 검색 URL 설정
    search_url = f"https://api.themoviedb.org/3/search/person"
    params = {
        "api_key": TMDB_API_KEY,
        "query": actor_name,
        "language": "ko-KR",
    }

    try:
        # 배우 검색 요청
        response = requests.get(search_url, params=params)
        data = response.json()

        # 검색 결과가 없을 경우 빈 리스트 반환
        if not data.get("results"):
            return []

        # 첫 번째 검색 결과의 ID를 사용하여 배우 ID 가져오기
        actor_id = data["results"][0]["id"]

        # 배우의 출연작 정보 요청
        movies_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
        }
        response = requests.get(movies_url, params=params)
        movies_data = response.json()

        # 상위 5개의 영화 정보를 추출하여 반환
        movies = []
        for movie in movies_data.get("cast", [])[:5]:
            movies.append({
                "title": movie["title"],
                "release_date": movie.get("release_date", ""),
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                "id": movie["id"],
            })

        return movies
    except Exception as e:
        print(f"TMDB API 오류: {str(e)}")
        return []


@csrf_exempt
def predict_actor(request):
    """
    POST로 전달된 이미지를 처리하여 모델 예측을 수행하고,
    닮은 배우와 그 배우의 출연작을 반환합니다.
    """
    try:
        # POST 요청만 허용
        if request.method != "POST":
            return JsonResponse({"error": "잘못된 요청입니다. POST 요청만 허용됩니다."}, status=400)

        # 이미지 파일 확인
        if "image" not in request.FILES:
            return JsonResponse({"error": "이미지가 포함되지 않았습니다."}, status=400)

        try:
            # 이미지 처리: PIL로 열어 크기 조정 및 정규화
            image = request.FILES["image"]
            img = Image.open(image).convert("RGB")
            img = img.resize((224, 224))  # Teachable Machine의 입력 크기
            img_array = np.expand_dims(np.array(img) / 255.0, axis=0)  # 모델 입력 형식에 맞게 변환
        except UnidentifiedImageError:
            return JsonResponse({"error": "유효하지 않은 이미지 파일입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"이미지 처리 중 오류 발생: {str(e)}"}, status=500)

        try:
            # 모델 로드 및 예측 수행
            if not os.path.exists(MODEL_PATH):
                return JsonResponse({"error": f"모델 경로를 찾을 수 없습니다: {MODEL_PATH}"}, status=500)

            model = tf.keras.models.load_model(MODEL_PATH)
            predictions = model.predict(img_array)  # 예측 수행
            max_index = np.argmax(predictions)  # 가장 높은 확률의 클래스 인덱스
        except Exception as e:
            return JsonResponse({"error": f"모델 예측 중 오류 발생: {str(e)}"}, status=500)

        try:
            # 라벨 파일 읽기
            if not os.path.exists(LABELS_PATH):
                return JsonResponse({"error": f"라벨 파일을 찾을 수 없습니다: {LABELS_PATH}"}, status=500)

            with open(LABELS_PATH, "r", encoding="utf-8") as f:
                labels = [line.strip() for line in f.readlines()]  # 줄 단위로 라벨 읽기
            actor_name = labels[max_index]  # 예측된 클래스의 라벨(배우 이름)
        except Exception as e:
            return JsonResponse({"error": f"라벨 로드 중 오류 발생: {str(e)}"}, status=500)

        try:
            # TMDB API를 통해 배우의 출연작 검색
            movies = get_actor_movies(actor_name)
        except Exception as e:
            return JsonResponse({"error": f"TMDB API 요청 중 오류 발생: {str(e)}"}, status=500)

        # 닮은 배우와 추천 영화 반환
        return JsonResponse({
            "actor": actor_name,
            "movies": movies,
        }, status=200)

    except Exception as e:
        # 예외 발생 시 오류 반환
        return JsonResponse({"error": f"서버 오류 발생: {str(e)}"}, status=500)
