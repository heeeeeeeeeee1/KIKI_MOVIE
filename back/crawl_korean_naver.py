import os
import requests
import shutil

# 네이버 검색 API 인증 정보
CLIENT_ID = "your_client_id"  # 네이버에서 발급받은 Client ID
CLIENT_SECRET = "your_client_secret"  # 네이버에서 발급받은 Client Secret

# 배우 목록
actors = [
    "강동원", "강소라", "강하늘", "고아성", "고현정", "공효진", "김고은", "김남길",
    "김민희", "김수현", "김태리", "김혜수", "남주혁", "류준열", "마동석", "박보영",
    "박서준", "박신혜", "박해일", "배두나", "배수지", "변요한", "손예진", "송강호",
    "송중기", "신민아", "안성기", "유아인", "유연석", "이병헌", "이정재", "이종석",
    "이주연", "임시완", "전도연", "전지현", "정우성", "조인성", "주지훈", "지창욱",
    "차승원", "최민식", "한지민", "한효주", "황정민", "현빈", "김윤석", "김희애",
    "이성민", "조진웅"
]

# 이미지 검색 함수
def search_images(query, count=50):
    url = "https://openapi.naver.com/v1/search/image"
    headers = {
        "X-Naver-Client-Id": 'cQ0aVGuj0Xs3b1EPZVty',
        "X-Naver-Client-Secret": 'NZUZoDHISy',
    }
    params = {
        "query": query,
        "display": count,  # 최대 50개
        "start": 1,
        "sort": "sim",  # 유사도 기반 정렬
        "filter": "large",  # 큰 이미지 필터링
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"이미지 검색 실패: {response.status_code}")
        return []

# 이미지 저장 함수
def save_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                shutil.copyfileobj(response.raw, file)
            print(f"이미지 저장 성공: {save_path}")
        else:
            print(f"이미지 저장 실패: {response.status_code} - {url}")
    except Exception as e:
        print(f"이미지 저장 중 오류 발생: {e}")

# 메인 로직
def main():
    base_dir = "actor_images"
    os.makedirs(base_dir, exist_ok=True)

    for actor in actors:
        print(f"'{actor}' 이미지 검색 중...")
        images = search_images(actor)

        actor_dir = os.path.join(base_dir, actor)
        os.makedirs(actor_dir, exist_ok=True)

        for i, image in enumerate(images):
            image_url = image.get("link")
            if not image_url:
                continue

            save_path = os.path.join(actor_dir, f"{actor}_{i + 1}.jpg")
            save_image(image_url, save_path)

if __name__ == "__main__":
    main()
