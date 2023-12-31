import pandas as pd
import selenium
from selenium import webdriver
from time import sleep
from tqdm import tqdm
from datetime import datetime, timedelta
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
from datetime import datetime, timedelta, date

# page_lists를 통해 얻은 뉴스게시판의 URL을 입력하여 각 뉴스의 URL을 list형태로 반환

def get_urls_naver(pages=None, agent='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Whale/3.21.192.18 Safari/537.36', 
             hidden_window=True, verbose=False):
    options = webdriver.ChromeOptions()
    options.add_argument(agent)
    if hidden_window:
        options.add_argument('headless') # 페이지 안 열기 
        options.add_argument('window-size=1920x1080') # 사이즈 지정
        options.add_argument("disable-gpu") # 안 보이게
    driver = webdriver.Chrome(options=options) # 창 열기
    driver.maximize_window() # 창 최대화

    # 크롤링 시작
    urls_week = [] # 한 주의 기사 리스트를 담을 큰 리스트 준비
    for i, page in enumerate(pages):
        urls_temp = []
        # 페이지 열기
        driver.get(url=page)
        sleep(0.5)
        
        # 해당 페이지가 1페이지인지 검사
        if i==0:
            driver.execute_script("window.scrollTo(0, 0)")
            try:
                click = driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[2]/div/a')
                sleep(1)
                click.click()
                sleep(1)
            except:
                pass
            # 헤드라인 담기
            for head in range(1, 9):
                selector = "#main_content > div > div._persist > div.section_headline > ul > li:nth-child(" +str(head)+ ") > div.sh_thumb > div > a"
                try:
                    headline_elems = driver.find_element_by_css_selector(selector)
                    headline_href = headline_elems.get_attribute("href")
                    urls_temp.append(headline_href)
                except:
                    pass

            # 연재1 담기
            for issue1 in range(1, 5):
                if issue1==1:
                    selector = "#main_content > div > div:nth-child(3) > div > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a"
                else:
                    selector = "#main_content > div > div:nth-child(3) > div > div.cluster_body > ul > li:nth-child("+str(issue1)+") > div > a"
                    
                try:
                    issue1_elems = driver.find_element_by_css_selector(selector)
                    issue1_href = issue1_elems.get_attribute("href")
                    urls_temp.append(issue1_href)
                except:
                    pass

            # 연재2 담기
            for issue2 in range(1, 5):
                if issue2==1:
                    selector = "#main_content > div > div:nth-child(4) > div > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a"
                else:
                    selector = "#main_content > div > div:nth-child(4) > div > div.cluster_body > ul > li:nth-child("+str(issue2)+") > div > a"
                
                try:
                    issue2_elems = driver.find_element_by_css_selector(selector)
                    issue2_href = issue2_elems.get_attribute("href")
                    urls_temp.append(issue2_href)
                except:
                    pass

        # 일반 기사의 URL 저장
        for norm_head in range(1, 6):
            selector = "#section_body > ul.type06_headline > li:nth-child("+str(norm_head)+") > dl > dt:nth-child(2) > a"
            try:
                norm_head_elems = driver.find_element_by_css_selector(selector)
                norm_head_href = norm_head_elems.get_attribute("href")
                urls_temp.append(norm_head_href)
            except:
                print("!!! norm_head 문제 발생 !!!")

        for norm_1 in range(1, 6):
            selector = "#section_body > ul:nth-child(2) > li:nth-child("+str(norm_1)+") > dl > dt:nth-child(2) > a"
            try:
                norm_1_elems = driver.find_element_by_css_selector(selector)
                norm_1_href = norm_1_elems.get_attribute("href")
                urls_temp.append(norm_1_href)
            except:
                print("!!! norm_1 문제 발생 !!!")

        for norm_2 in range(1, 6):
            selector = "#section_body > ul:nth-child(3) > li:nth-child("+str(norm_2)+") > dl > dt:nth-child(2) > a"
            try:
                norm_2_elems = driver.find_element_by_css_selector(selector)
                norm_2_href = norm_2_elems.get_attribute("href")
                urls_temp.append(norm_2_href)
            except:
                print("!!! norm_2 문제 발생 !!!")

        for norm_3 in range(1, 6):
            selector = "#section_body > ul:nth-child(4) > li:nth-child("+str(norm_3)+") > dl > dt:nth-child(2) > a"
            try:
                norm_3_elems = driver.find_element_by_css_selector(selector)
                norm_3_href = norm_3_elems.get_attribute("href")
                urls_temp.append(norm_3_href)
            except:
                print("!!! norm_3 문제 발생 !!!")
        
        # 마지막으로, 페이지 내의 url들 담기
        urls_week.append(urls_temp)
        if verbose:
            print(str(i+1)+'번째 페이지 url 저장 성공')
            print(len(urls_temp), "개의 URL 저장 성공")
            print("*"*50)

    # 크롬드라이버 종료
    driver.quit()

    # 중복 제거
    count = 0
    prepared_urls = []
    for idx in range(len(urls_week)):
        count += len(urls_week[idx])
        for url in urls_week[idx]:
            # 중복 제거를 위해 이미 담겨있는지 확인
            if url not in prepared_urls: 
                prepared_urls.append(url)
                
    # 차후 conplict 방지를 위해 hotissue를 지운 url로 통일
    prepared_urls = [url.replace("/hotissue/", "/")  for url in prepared_urls]
            
    print("중복 제거 전 URL 수 :", count)
    print("중복 제거 후 URL 수 :", len(prepared_urls))

    return prepared_urls


# 크롤링 수행한 후 DataFrame형식으로 반환
def news_crawler_naver(df, agent='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                 hidden_window=False):
    options = webdriver.ChromeOptions()
    options.add_argument(agent)
    if hidden_window:
        options.add_argument('headless') # 페이지 안 열기 
        options.add_argument('window-size=1920x1080') # 사이즈 지정
        options.add_argument("disable-gpu") # 안 보이게
    driver = webdriver.Chrome(options=options) # 창 열기
    driver.maximize_window() # 창 최대화

    # 크롤링 수행
    for idx in tqdm(range(len(df))):
        link = df.loc[idx, 'URL']
        driver.get(link)
        sleep(0.5)
        
        # 날짜
        date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span"
        date_elems = driver.find_element_by_css_selector(date_selector)
        date = date_elems.text[:10].replace('.', '-')

        # 시간
        time_selector = '#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span'
        time_elems = driver.find_element_by_css_selector(time_selector)

        # 24시간 내에 해당하는지 검사
        now = datetime.now()
        article_time = time_elems.text
        article_time = article_time.split('.')
        year = int(article_time[0])
        month = int(article_time[1])
        day = int(article_time[2])
        times = article_time[-1]
        if '오전' in time_elems.text: # 오전의 경우
            temp_time = article_time[3].replace('오전 ', '')
            temp_time = temp_time.split(':')
            hour = int(temp_time[0].strip())
            minute = int(temp_time[-1].strip())
        else: # 오후의 경우
            temp_time = article_time[3].replace('오후 ', '')
            temp_time = temp_time.split(':')
            hour = int(temp_time[0].strip())+12
            if int(temp_time[0].strip())==12:
                hour = int(temp_time[0].strip())
            minute = int(temp_time[-1].strip())

        #print(year, month, day, hour, minute)
        target_time = datetime(year, month, day, hour, minute) # 기사가 개제된 시간
        time_limit = datetime.now() - timedelta(days=1) # 현재로부터 24시간 전
        if target_time < time_limit:
            df = df.drop([idx], axis=0)
            continue


        # 신문사
        company_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type"
        company_elems = driver.find_element_by_css_selector(company_selector)
        company = company_elems.get_attribute("title")
        
        # 기자명
        reporter_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_journalist > a > em"
        try:
            reporter_elems = driver.find_element_by_css_selector(reporter_selector)
            reporter = reporter_elems.text
        except:
            reporter = "정보없음"
        reporter = reporter.replace(" 기자", '')
        
        # 제목
        title_selector = "#title_area > span"
        title_elems = driver.find_element_by_css_selector(title_selector)
        title = title_elems.text
        
        # 본문
        text_selector = "#dic_area"
        text_elems = driver.find_element_by_css_selector(text_selector)
        text = text_elems.text
        
        # 수집한 데이터를 데이터프레임에 추가
        df.loc[idx, '날짜'] = date
        df.loc[idx, '신문사'] = company
        df.loc[idx, '기자명'] = reporter
        df.loc[idx, '제목'] = title
        df.loc[idx, '본문'] = text

    driver.quit()
        
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    df['요일'] = df['날짜'].dt.dayofweek
    
    # 마지막으로 중복 제거 및 인덱스 재설정
    df.drop_duplicates(subset=['제목'], keep='last', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df




# 일주일 단위로 it 전체 기사 링크 저장하기
def get_urls_daum(end_page=100, agent="user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", hidden_window=False):
    today = date.today()
    end_date = today.strftime("%Y%m%d")

    yesterday = today - timedelta(days=1)
    start_date = yesterday.strftime("%Y%m%d")

    base_url = "https://news.daum.net/breakingnews/digital?page="
    options = webdriver.ChromeOptions()
    options.add_argument(agent)
    if hidden_window:
        options.add_argument('headless')  
        options.add_argument('window-size=1920x1080') 
        options.add_argument("disable-gpu") 
    driver = webdriver.Chrome(options=options)

    link_list = []

    current_date = int(start_date)
    while current_date <= int(end_date):
        current_page = 1
        while current_page <= int(end_page):
            url = f"{base_url}{current_page}&regDate={current_date}"
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.box_etc ul.list_news2 li div strong a')))
                time.sleep(0.25)
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


# 뉴스 정보 저장
def news_crawler_daum(df, agent="user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"):
    from datetime import date
    today = date.today()
    end_date = today.strftime("%Y%m%d")
    yesterday = today - timedelta(days=1)

    start_date = yesterday.strftime("%Y%m%d")

    options = webdriver.ChromeOptions()
    options.add_argument(agent)
    options.add_argument('headless') 
    options.add_argument('window-size=1920x1080') 
    options.add_argument("disable-gpu") 
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)

    for index in tqdm(range(len(df.index))):
        url = df.loc[index, 'URL']
        driver.get(url)
        time.sleep(0.25)

        # 날짜 및 시간
        try:
            date_elems = driver.find_element_by_css_selector('#mArticle > div.head_view > div.info_view > span:nth-child(2) > span').text
            date = date_elems[:11].replace('.', '-')
        except:
            try:
                date_elems = driver.find_element_by_css_selector('#mArticle > div.head_view > div.info_view > span > span').text
                date = date_elems[:11].replace('.', '-')
            except Exception as e:
                print(f"An exception occurred: {str(e)}")

        # 24시간 내에 있는지
        article_time = date_elems.split('.')
        year = int(article_time[0])
        month = int(article_time[1])
        day = int(article_time[2])
        times = article_time[-1]
        temp_time = times.split(':')
        hour = int(temp_time[0].strip())
        minute = int(temp_time[-1].strip())
        
        # 기사가 작성된 시간
        target_time = datetime(year, month, day, hour, minute)
        # 현재부터 24시간 전
        time_limit = datetime.now() - timedelta(hours=24)
        
        if target_time < time_limit:
            df = df.drop([index], axis=0)
            continue
        
        # 신문사
        company = driver.find_element_by_css_selector('#kakaoServiceLogo').text

        # 기자명
        try:
            reporter = driver.find_element_by_css_selector('#mArticle > div.head_view > div.info_view > span:nth-child(1)').text
            reporter = re.sub(r'\[|\]|\(|\)', '', reporter)
            if '인턴' in reporter:
                reporter = reporter.replace('인턴', '').split(' ')[0]
            elif reporter == '입력':
                reporter = '정보없음'
            else:
                reporter = reporter.split(' ')[0]
        except:
            reporter = '정보없음'
        
        # 제목
        title = driver.find_element_by_css_selector('#mArticle > div.head_view > h3').text
        
        # 본문
        context = driver.find_element_by_css_selector('#mArticle > div.news_view.fs_type1').text
            
        # DataFrame에 값 추가
        df.loc[index, '날짜'] = date
        df.loc[index, '신문사'] = company
        df.loc[index, '기자명'] = reporter
        df.loc[index, '제목'] = title
        df.loc[index, '본문'] = context        
        
    driver.quit()

    df = df.assign(날짜=pd.to_datetime(df['날짜']))
    df = df.assign(연=df['날짜'].dt.year)
    df = df.assign(월=df['날짜'].dt.month)
    df = df.assign(일=df['날짜'].dt.day)
    df = df.assign(요일=df['날짜'].dt.weekday)

    df.drop_duplicates(subset=['기자명', '제목'], inplace=True)

    return df

# df.reset_index(drop=True, inplace=True)

# df.to_csv(f'{start_date}_{end_date}_news.csv', index=False)
# print("news_data 저장 완료.")











