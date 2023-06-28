from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from selenium.webdriver.common.keys import Keys
import pyperclip
import pyautogui
from selenium.webdriver.chrome.options import Options

def get_comments(blog_post_url):
    driver.get(blog_post_url)

    # 페이지의 소스를 가져옵니다.
    html = driver.page_source

    # BeautifulSoup 객체를 생성합니다.
    soup = BeautifulSoup(html, 'html.parser')

    # 페이지에 iframe이 있는지 확인합니다.
    iframes = soup.find_all('iframe')
    if (iframes):
        driver.switch_to.frame('mainFrame')

    # 이제 iframe 내부의 요소들을 선택할 수 있습니다.
    comment_button = driver.find_elements(By.CLASS_NAME, 'btn_comment')
    comment_button[1].click()

    # 댓글이 로드될 때까지 잠시 대기합니다.
    time.sleep(2)
    html = driver.page_source

    # BeautifulSoup 객체를 생성합니다.
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_comments(soup):
    # 댓글 부분을 찾습니다.
    comment_area = soup.find('div', {'class': 'u_cbox_content_wrap'})
    # 댓글 내용
    comments = [comment.text for comment in comment_area.find_all('span', {'class': 'u_cbox_contents'})]
    # 이름
    nicks = [nick.text for nick in comment_area.find_all('span', {'class': 'u_cbox_nick'})]
    # 작성 일자
    dates = [date.text for date in comment_area.find_all('span', {'class': 'u_cbox_date'})]

    return list(zip(nicks, comments, dates))  # 각각의 댓글 정보를 하나의 튜플로 묶어서 리스트로 반환합니다.


def save_to_excel(comments):
    # 데이터를 DataFrame으로 변환합니다.
    df = pd.DataFrame(comments, columns=['Name', 'Comment', 'Date'])

    # DataFrame을 엑셀 파일로 저장합니다.
    df.to_excel('comments.xlsx', index=False)  # 'comments.xlsx'는 저장하려는 파일 이름입니다.


import pickle


import os
import json

import pyautogui
from selenium import webdriver

import os
import json
from selenium.common.exceptions import NoSuchElementException

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def login_naver():
    # Check if cookies.json exists
    if os.path.exists('cookies.json'):
        # Load the cookies from file
        driver.get('https://www.naver.com')
        cookies = json.load(open('cookies.json'))
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        # User login manually and cookies are saved to cookies.json
        driver.get('https://nid.naver.com/nidlogin.login')
        input("Please log in manually and then press Enter here... ")
        cookies = driver.get_cookies()
        json.dump(cookies, open('cookies.json', 'w'))

    # Reload page
    driver.get('https://www.naver.com')

    # Check if user is logged in
    try:
        log_status = driver.find_element(By.CLASS_NAME, 'link_login_help').text
        if log_status:
            print('Login successful')
            cookies = driver.get_cookies()
            json.dump(cookies, open('cookies.json', 'w'))
        else:
            print('Login failed')
            if os.path.exists('cookies.json'):
                os.remove('cookies.json')
    except NoSuchElementException:
        print("Login check element not found")
        pass



# Chrome 웹 드라이버의 경로를 입력하세요.
options = Options()
# options.add_argument("--headless")  # 헤드리스 모드 활성화를 위한 줄입니다. 주석 처리하여 헤드리스 모드를 비활성화합니다.
webdriver_service = Service('./chromedriver')
driver = webdriver.Chrome(service=webdriver_service,options=options)

# driver = webdriver.Chrome()


login_naver()  # 로그인
blog_post_url = 'https://blog.naver.com/windylung/223049315704'# 실제 블로그 포스트의 URL을 입력하세요.
soup = get_comments(blog_post_url)
comments = extract_comments(soup)
save_to_excel(comments)
print('완료했습니다.')