# -*- coding: utf-8 -*-

# 필요 패키지 호출
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import csv

# 함수 정의: 검색어 조건에 따른 url 생성
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + str(word)
    return url

# 함수 정의: 열린 페이지에서 첫 번째 게시물 클릭 + sleep 메소드 통하여 시차 두기
def select_first(driver):
    first = driver.find_elements_by_css_selector("div._9AhH0")[0]
    first.click()
    time.sleep(5)


def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 본문 내용
    try:
        content = soup.select('div.MOdxS')[0].text
    except:
        content = ''
    # 해시태그
    tags = re.findall(r'#[^\s#,\\]+', content)

    # 작성일자
    #date = soup.select('time._1o9PC')[0]['datetime'][:10]

    # 좋아요
    #try:
    #    like = soup.select('section.EDfFK.ygqzn')[0].findAll('span')[-1].text
    #except:
    #    like = 0
    # 위치
    #try:
    #    place = soup.select('div.M30cS')[0].text
    #except:
    #    place = ''
    data = [content, tags]#, date, like, place, tags]
    return data

# 함수 정의: 첫 번째 게시물 클릭 후 다음 게시물 클릭
def move_next(driver):
    right = driver.find_element_by_css_selector('div.l8mY4.feth3')
    right.click()
    time.sleep(3)

# 크롬 브라우저 열기
driver = webdriver.Chrome('chromedriver')
#driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
#driver = webdriver.Firefox(executable_path='./geckodriver')

driver.get('https://www.instagram.com')
time.sleep(3)

# 인스타그램 로그인을 위한 계정 정보
email = '01025575493'
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = 'RickyLee23#'
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)

#word = input('검색어를 입력하세요 : ')
word = str('믿음')
url = insta_searching(word)

# 검색 결과 페이지 열기
driver.get(url)
time.sleep(8)

# 첫 번째 게시물 클릭
select_first(driver)

# 본격적으로 데이터 수집 시작
results = []

# 수집할 게시물의 수
target = 10000
count = 0

f = open('./%s.csv'%word, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(['no','text','tags','emotion'])

def text_count(text):
    clean_text = ''
    for i in text:
        if i == '#':
            break
        else:
            clean_text += i
        
    return clean_text, len(clean_text)

for i in range(target):
    try:
        data = get_content(driver)
        
        # 유효한 데이터 필터링
        text, text_len = text_count(data[0])

        if text_len>=50:
            results.append(data)
            count += 1
            print('[%d/%d]'%(count,i), text)

            # csv 저장
            wr.writerow([count,text,data[1],'%s'%word])
        move_next(driver)

        if count == 100:
            break
    except:
        print('!!! except occur !!!')
        time.sleep(2)
        move_next(driver)

f.close()
print('%s Done.'%word)

