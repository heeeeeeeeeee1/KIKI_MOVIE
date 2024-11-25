# 크롤링으로 추가 데이터 수집
import os
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ChromeDriver 자동 설치
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# 이미지 다운로드 함수
def download_images(search_query, save_dir, max_images=60):
    driver = webdriver.Chrome(service=service, options=options)
    url = f"https://www.google.com/search?q={search_query}+portrait&tbm=isch"
    driver.get(url)

    # 이미지 URL 저장
    image_urls = set()

    # 스크롤하며 이미지 수집
    for _ in range(15):  # 스크롤 15번 (더 많은 이미지 로드)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # 이미지 로딩 시간 대기
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            src = img.get_attribute("src")
            if src and "http" in src:
                image_urls.add(src)
        if len(image_urls) >= max_images:  # 최대 이미지 개수 도달
            break

    # 이미지 다운로드
    os.makedirs(save_dir, exist_ok=True)
    count = 0
    for url in image_urls:
        if count >= max_images:
            break
        try:
            img_data = requests.get(url).content
            safe_name = search_query.replace(" ", "_").replace("/", "_")
            with open(f"{save_dir}/{safe_name}_{count + 1}.jpg", "wb") as img_file:
                img_file.write(img_data)
                count += 1
        except Exception as e:
            print(f"이미지 다운로드 실패: {e}")

    driver.quit()
    print(f"{search_query} - {count}장 다운로드 완료.")

# 배우 이미지 데이터 다운로드
def fetch_actor_training_data():
    # 배우 목록 불러오기
    with open("top_actors.json", "r", encoding="utf-8") as f:
        actors = json.load(f)

    # 배우당 이미지 60장 다운로드
    for actor in actors:
        actor_name = actor["fields"]["name"]
        save_dir = f"actor_images_training/{actor_name.replace(' ', '_').replace('/', '_')}"
        download_images(actor_name, save_dir, max_images=60)

# 실행
fetch_actor_training_data()
