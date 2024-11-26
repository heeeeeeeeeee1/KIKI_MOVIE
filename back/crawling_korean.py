import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote  # URL 인코딩을 위한 quote 함수

# Chrome WebDriver 설정
options = Options()
options.add_argument("--start-maximized")  # 브라우저 최대화
options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 감지 비활성화
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# 필요하면 브라우저를 숨기려면 아래 주석 해제 (헤드리스 모드)
# options.add_argument("--headless")

# 배우들의 이름 목록
actors = [
    "강동원", "강소라", "강하늘", "고아성", "고현정", "공효진", "김고은", "김남길",
    "김민희", "김수현", "김태리", "김혜수", "남주혁", "류준열", "마동석", "박보영",
    "박서준", "박신혜", "박해일", "배두나", "배수지", "변요한", "손예진", "송강호",
    "송중기", "신민아", "안성기", "유아인", "유연석", "이병헌", "이정재", "이종석",
    "이주연", "임시완", "전도연", "전지현", "정우성", "조인성", "주지훈", "지창욱",
    "차승원", "최민식", "한지민", "한효주", "황정민", "현빈", "김윤석", "김희애",
    "이성민", "조진웅"
]

# 이미지 다운로드 함수
def download_images(search_query, save_dir, max_images=60):
    # ChromeDriver 초기화
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 구글 이미지 검색 URL 생성
    encoded_query = quote(f"{search_query} 셀카")  # '셀카' 키워드 추가
    url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&tbs=isz:l"
    driver.get(url)
    
    # 이미지 URL 저장
    image_urls = set()
    
    # 스크롤 동작
    for _ in range(15):  # 스크롤 15번 실행
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        
        images = driver.find_elements(By.CSS_SELECTOR, 'img')
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)
            if len(image_urls) >= max_images:
                break
    
    # 이미지 다운로드
    os.makedirs(save_dir, exist_ok=True)
    count = 0
    
    for url in image_urls:
        if count >= max_images:
            break
        try:
            img_data = requests.get(url).content
            safe_name = search_query.replace(" ", "_")
            with open(f"{save_dir}/{safe_name}_{count + 1}.jpg", 'wb') as img_file:
                img_file.write(img_data)
            count += 1
        except Exception as e:
            print(f"이미지 다운로드 실패: {e}")
    
    driver.quit()
    print(f"{search_query} - {count}장 다운로드 완료.")

# 배우 이미지 데이터 다운로드
def fetch_actor_images():
    base_dir = 'actors_images'
    for actor in actors:
        actor_dir = os.path.join(base_dir, actor.replace(" ", "_"))
        download_images(actor, actor_dir, max_images=60)

# 실행
if __name__ == "__main__":
    fetch_actor_images()
