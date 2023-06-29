import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def ensure_mobile_url(url):
    if "m.blog.naver.com" not in url:
        url = url.replace("blog.naver.com", "m.blog.naver.com")
    return url

def extract_comments(driver, url, num_scrolls):
    driver.get(url)
    time.sleep(2)  # 페이지가 완전히 로드될 때까지 잠시 대기

    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    comment_area = soup.find('div', {'class': 'u_cbox_content_wrap'})

    if comment_area is None:
        print('No comment area found')
        return []

    # 댓글 내용
    comments = [comment.text for comment in comment_area.find_all('span', {'class': 'u_cbox_contents'})]
    # 이름
    nicks = [nick.text for nick in comment_area.find_all('span', {'class': 'u_cbox_nick'})]
    # 작성 일자
    dates = [date.text for date in comment_area.find_all('span', {'class': 'u_cbox_date'})]

    comments = list(zip(nicks, comments, dates))  # 각각의 댓글 정보를 하나의 튜플로 묶어서 리스트로 반환합니다.
    return comments


def get_comment_url_and_num_scrolls(driver, url):
    # 블로그 페이지로 이동
    driver.get(url)

    # 페이지가 로드될 때까지 잠시 기다립니다.
    time.sleep(2)

    # btn_reply 클래스의 a 태그를 찾습니다.
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find('a', class_='btn_reply')
    href = a_tag.get('href')

    # 새 URL 생성
    new_url = f"https://m.blog.naver.com{href}"

    # 댓글 수 가져오기
    num_comments = int(a_tag.find('em').text.replace(',', ''))
    num_scrolls = num_comments // 100 + 1

    print(new_url, num_scrolls)
    return new_url, num_scrolls


def save_to_excel(comments):
    # 데이터 프레임을 생성하고 댓글을 저장
    df = pd.DataFrame(comments, columns=['Name', 'Comment', 'Date'])
    df.to_excel('comments.xlsx', index=False)


options = Options()
options.add_argument("--headless")  # 헤드리스 모드 활성화를 위한 줄입니다. 주석 처리하여 헤드리스 모드를 비활성화합니다.
webdriver_service = Service('./chromedriver')
driver = webdriver.Chrome(service=webdriver_service, options=options)

# 첫 번째 페이지의 URL
url = "https://blog.naver.com/pepilogue/223127983042"
url = ensure_mobile_url(url)
# 댓글이 있는 페이지의 URL을 가져옵니다.
new_url, num_scrolls = get_comment_url_and_num_scrolls(driver, url)

# 새 URL에서 댓글을 추출
comments = extract_comments(driver, new_url, num_scrolls)

# 추출한 댓글을 엑셀 파일로 저장합니다.
save_to_excel(comments)

# WebDriver를 닫습니다.
driver.quit()
