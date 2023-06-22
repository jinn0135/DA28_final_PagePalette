import pandas as pd
import numpy as np
import csv
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# 일주일 단위로 it 전체 기사 링크 저장하기
def link_scraper(start_date, end_date, end_page):
    base_url = "https://news.daum.net/breakingnews/digital?page="

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument('headless')  
    options.add_argument('window-size=1920x1080') 
    options.add_argument("disable-gpu") 
    driver = webdriver.Chrome(options=options)

    link_list = []

    current_date = int(start_date)
    while current_date <= int(end_date):
        current_page = 1
        while current_page <= int(input(end_page)):
            url = f"{base_url}{current_page}&regDate={current_date}"
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.box_etc ul.list_news2 li div strong a')))
                time.sleep(1)
                articles = driver.find_elements(By.CSS_SELECTOR, 'div.box_etc ul.list_news2 li div strong a')
                if not articles:
                    break
                for article in articles:
                    href = article.get_property('href')
                    if href not in link_list:
                        link_list.append(href)
                current_page += 1
            except Exception as e:
                print(f"An exception occurred: {str(e)}")
                break
                        
        current_date += 1

    driver.quit()

    return link_list

# filename = f"link_{start_date}_{end_date}.csv"
# with open(filename, "w", newline="\n") as file:
#     writer = csv.writer(file)
#     for list in link_list:
#         writer.writerow([list])

# print(f"{filename}저장 완료.")

# 링크 csv 파일 -> 데이터 프레임으로 생성
def make_df(file):
    df = pd.DataFrame()
    df_list = pd.read_csv(file, names=['URL'])
    df = pd.concat([df, df_list], axis=0, ignore_index=True)

    new_columns = ['신문사', '기자명', '제목', '본문', '날짜', '연', '월', '일', '요일']
    df = pd.concat([df, pd.DataFrame(columns=new_columns)], axis=1)
    
    return df

# 뉴스 정보 저장
def news_data(start_date, end_date, df):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument('headless') 
    options.add_argument('window-size=1920x1080') 
    options.add_argument("disable-gpu") 
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)

    for index in tqdm(range(len(df.index))):
        url = df.loc[index, 'URL']
        driver.get(url)
        time.sleep(0.5)
        
        # 신문사
        company = driver.find_element_by_css_selector('#kakaoServiceLogo').text

        # 기자명
        reporter = driver.find_element_by_css_selector('#mArticle > div.head_view > div.info_view > span:nth-child(1)').text
        reporter = re.sub(r'\[|\]|\(|\)', '', reporter)
        if '인턴' in reporter:
            reporter = reporter.replace('인턴', '').split(' ')[0]
        elif reporter == '입력':
            reporter = '정보없음'
        else:
            reporter = reporter.split(' ')[0]
        
        # 제목
        title = driver.find_element_by_css_selector('#mArticle > div.head_view > h3').text
        
        # 본문
        context = driver.find_element_by_css_selector('#mArticle > div.news_view.fs_type1').text
        
        # 날짜
        date = df.loc[index, 'URL'].split('/')[-1][:8]
        
        # DataFrame에 값 추가
        df.loc[index, '신문사'] = company
        df.loc[index, '기자명'] = reporter
        df.loc[index, '제목'] = title
        df.loc[index, '본문'] = context
        df.loc[index, '날짜'] = date
        
    driver.quit()

    df = df.assign(날짜=pd.to_datetime(df['날짜']))
    df = df.assign(연=df['날짜'].dt.year)
    df = df.assign(월=df['날짜'].dt.month)
    df = df.assign(일=df['날짜'].dt.day)
    df = df.assign(요일=df['날짜'].dt.weekday)

    return df

# df.drop_duplicates(subset=['기자명', '제목'], inplace=True)
# df.to_csv(f'{start_date}_{end_date}_news.csv', index=False)

# print("news_data 저장 완료.")