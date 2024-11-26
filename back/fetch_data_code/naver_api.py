# naver 검색 api로 배우 이미지 수집
import os
import requests
import json

# 네이버 API 키 설정
CLIENT_ID = ""  # 네이버에서 발급받은 Client ID
CLIENT_SECRET = ""  # 네이버에서 발급받은 Client Secret

# 네이버 이미지 검색 API 요청 함수
def search_images(keyword, display=10, start=1):
    url = "https://openapi.naver.com/v1/search/image"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": keyword,
        "display": display,  # 가져올 이미지 수
        "start": start,  # 시작 인덱스
        "sort": "sim"  # 유사도 순
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 요청 실패: {response.status_code}, {response.text}")
        return None


# 이미지 다운로드 함수
def download_images(keyword, save_dir="images", num_images=50):
    os.makedirs(save_dir, exist_ok=True)
    current_count = 0
    start_index = 1

    while current_count < num_images:
        result = search_images(keyword, display=10, start=start_index)
        if not result or "items" not in result:
            print(f"{keyword}에 대한 이미지를 찾을 수 없습니다.")
            break

        for item in result["items"]:
            if current_count >= num_images:
                break
            try:
                img_url = item["link"]
                img_data = requests.get(img_url, timeout=5).content
                img_filename = os.path.join(save_dir, f"{keyword}_{current_count + 1}.jpg")

                with open(img_filename, "wb") as img_file:
                    img_file.write(img_data)
                    print(f"{keyword} 이미지 저장 완료: {img_filename}")
                current_count += 1
            except Exception as e:
                print(f"이미지 다운로드 실패: {e}")

        start_index += 10   # 결과 10개씩 가져오기


# 배우 이미지 다운로드 실행 함수
def download_actor_images():
    with open("top_actors.json", "r", encoding="utf-8") as f:
        actors = json.load(f)

    os.makedirs("training_data", exist_ok=True)

    for actor in actors:
        actor_name = actor["fields"]["name"]
        actor_dir = os.path.join("training_data", actor_name.replace(" ", "_"))
        os.makedirs(actor_dir, exist_ok=True)

        print(f"{actor_name} 이미지 다운로드 시작...")
        download_images(actor_name, save_dir=actor_dir, num_images=50)
        print(f"{actor_name} 이미지 다운로드 완료.")


# 실행
download_actor_images()
