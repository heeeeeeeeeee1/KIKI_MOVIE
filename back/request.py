import requests
import json
from django.conf import settings

API_KEY = settings.TMDB_API_KEY
BASE_URL = 'https://api.themoviedb.org/3'
LAST_PAGE = 4    # TMDB API의 한 페이지에 포함된 데이터: 기본적으로 20개의 항목(4페이지라면 20*4)

# TMDB API 요청 함수
def response_data(url):
    response = requests.get(url)
    return response.json()


# json 데이터 저장
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{filename} 생성")


# 출연진 및 감독 저장
def fetch_credits():
    actors_data = []
    directors_data = []

    for PAGE in range(1, LAST_PAGE + 1):
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page={PAGE}'
        data = response_data(url)

        for movie in data.get('results', []):
            movie_id = movie['id']
            credits_url = f'{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=ko-KR'
            credits_data = response_data(credits_url)

            # 배우 저장
            for cast in credits_data.get('cast', []):
                if cast['id'] not in [actor['pk'] for actor in actors_data]:
                    actors_data.append({
                        "model": "movies.Actor",
                        "pk": cast['id'],
                        "fields": {
                            "name": cast['name'],
                            "profile_path": cast.get('profile_path', '')
                        }
                    })

            # 감독 저장
            for crew in credits_data.get('crew', []):
                if crew['job'] == 'Director':
                    if crew['id'] not in [director['pk'] for director in directors_data]:
                        directors_data.append({
                            "model": "movies.Director",
                            "pk": crew['id'],
                            "fields": {
                                "name": crew['name'],
                                "profile_path": crew.get('profile_path', '')
                            }
                        })

    save_to_json(actors_data, 'actors.json')
    save_to_json(directors_data, 'directors.json')



# 장르 데이터 가져오기 및 json 파일 저장
def fetch_genres():
    genres_data = []
    url = f'{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=ko-KR' 
    data = response_data(url)

    for genre in data.get('genres', []):
        genres_data.append({
            "model": "movies.Genre",
            "pk": genre['id'],
            "fields": {
                "name": genre['name']
            }
        })
    save_to_json(genres_data, 'genres.json')


# 영화 상세 정보 가져오기
def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=ko-KR"
    data = response_data(url)

    return {
        "runtime": data.get("runtime", None),
        "status": data.get("status", None),
        "tagline": data.get("tagline", None),
        "genres": [genre["id"] for genre in data.get("genres", [])]  # 장르 ID 리스트 반환
    }


# 영화 데이터 가져오기 및 json 파일 저장
def fetch_movies():
    movies_data = []

    for PAGE in range(1, LAST_PAGE + 1):
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page={PAGE}'
        data = response_data(url)
        movies = data.get('results',[])  # result 값 가져오고, 못 가져오면 빈리스트(기본값)

        for movie in movies:  # movie는 딕셔너리
            # 상세 정보 가져오기
            additional_details = fetch_movie_details(movie['id'])   # 위에서 정의한 영화 상세 정보 가져오는 함수 활용

            movies_data.append({
                "model": "movies.Movie",  # 'app_name'을 Django 앱 이름으로 변경
                "pk": movie['id'],  # 기본 키
                "fields": {
                    "id": movie['id'],
                    'title': movie['title'],
                    'original_title': movie['original_title'],
                    'description': movie['overview'],
                    'release_date': movie['release_date'],
                    # "created_at": current_date,  # 현재 날짜 추가
                    'vote_average': movie['vote_average'], 
                    'poster_path': movie['poster_path'],
                    # 'video_path': video_path,  # 비디오 경로 추가
                    'popularity': movie['popularity'],
                    'runtime': additional_details['runtime'],  # 상세 정보에서 가져온 데이터
                    'status': additional_details['status'],    # 상세 정보에서 가져온 데이터
                    'tagline': additional_details['tagline'],  # 상세 정보에서 가져온 데이터
                    'adult': movie['adult'],
                    # 'genre': ", ".join(genres),  # 장르 이름을 쉼표로 구분한 문자열  
                }
            })    
    save_to_json(movies_data, 'movies.json')



# 비디오 경로 가져오기 및 json 파일 저장
def fetch_videos():
    videos_data = []

    for PAGE in range(1, LAST_PAGE + 1):
    # 영화 정보가 있어야 비디오 가져올 수 있음(movie_id 사용)
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page={PAGE}"
        data = response_data(url)
        movies = data.get('results',[])

        for movie in movies:
            movie_id = movie["id"]  # 영화 ID
            video_url = f"{BASE_URL}/movie/{movie_id}/videos?api_key={API_KEY}&language=ko-KR"
            video_data = response_data(video_url)

            for video in video_data.get("results", []):
                if video["site"] == "YouTube":  # 유튜브 비디오만 저장
                    videos_data.append({
                        "model": "movies.Video",
                        "pk": video["id"],  # 비디오 ID
                        "fields": {
                            "name": video["name"],
                            "key": video["key"],  # 유튜브 비디오 키
                            "video_type": video["type"],  # 예: Trailer
                            "site": video["site"],  # 예: YouTube
                            "movie": movie_id  # 비디오가 속한 영화의 ID
                        }
                    })
    # 비디오 데이터를 JSON 파일로 저장
    save_to_json(videos_data, "videos.json")



# 키워드 데이터 가져오기 및 저장
def fetch_keywords():
    keywords_data = []
    for PAGE in range(1, LAST_PAGE + 1):
        # 영화 정보가 있어야 비디오 가져올 수 있음(movie_id 사용)
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page={PAGE}"  # 영화 목록 가져오기
        movies = response_data(url).get("results", [])

        for movie in movies:
            movie_id = movie["id"]
            keywords_url = f"{BASE_URL}/movie/{movie_id}/keywords?api_key={API_KEY}"  # 영화의 키워드 가져오기
            data = response_data(keywords_url)
            keywords = data.get("keywords", [])

            for keyword in keywords:
                if keyword["id"] not in [kw["pk"] for kw in keywords_data]: # 키워드 리스트에 없으면 추가
                    keywords_data.append({
                        "model": "movies.Keyword",
                        "pk": keyword["id"],
                        "fields": {
                            "name": keyword["name"]
                        }
                    })
    save_to_json(keywords_data, "keywords.json")


# 실행
fetch_genres()         # 장르 데이터 저장
fetch_movies()         # 영화 데이터 저장
fetch_credits()        # 배우 및 감독 데이터 저장
fetch_videos()  # 비디오 데이터 저장
fetch_keywords()       # 키워드 데이터 저장

