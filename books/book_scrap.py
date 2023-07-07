import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import re, time
from datetime import datetime
import pickle

import pymysql 
import pandas as pd 
import numpy as np
from tqdm import tqdm

# 장르별로 크롤링하기 
class createDB():
    def __init__(self, genres={'소설':'01', '시에세이':'03', '인문':'05', '경제경영':'13', 
                                '자기계발':'15', '정치사회':'17', '역사문화':'19', 
                                '예술대중문화':'23', '과학':'29' }):
#         genres={'요리': '08', '건강':'09', '가정육아':'07', '청소년':'38', '여행':'32', '여행에세이':'3204'}
        self.genres = genres
        self.urls, self.dfs = {}, {}
        
    def open_driver(self, url, scroll=False): # chrome driver 연결
        user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument(user_agent)
        options.add_argument('headless') # 페이지 안 열기 
        options.add_argument('window-size=1920x1080') # 사이즈 지정
        options.add_argument("disable-gpu") # 안 보이게
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        
        if scroll: # 페이지 맨 아래까지 스크롤
            prev_height = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
                curr_height = self.driver.execute_script('return document.body.scrollHeight')
                if prev_height == curr_height: break
                prev_height = curr_height
        
    def save_urls(self, genre): # 베스트셀러 페이지에서 각 장르의 도서 url들 저장
        self.urls[genre] = {}
        tqdm_pages = tqdm(range(20,0,-1))
        for page in tqdm_pages: # 한 페이지 당 50권, 20페이지 반복(1000위까지)
            url = 'https://product.kyobobook.co.kr/category/KOR/{}#?page={}&type=best&per=50'.format(self.genres[genre], page)
            self.open_driver(url)
            best = self.driver.find_element_by_css_selector('#homeTabBest')
            elems = best.find_elements_by_class_name('prod_info_box')
            for elem in elems:
                title = elem.find_element_by_css_selector('.prod_name').text
                rank = elem.find_element_by_class_name('text').text
                author = elem.find_element_by_css_selector('.prod_author > a').text
                temp_url = elem.find_element_by_class_name('prod_info')
                url = temp_url.get_attribute('href')
                temp_rate = elem.find_element_by_class_name('review_klover_box')
                rate = temp_rate.find_element(By.TAG_NAME, 'span').text

                self.urls[genre][title] = {}
                self.urls[genre][title]['url'] = url
                self.urls[genre][title]['rank'] = rank
                self.urls[genre][title]['author'] = author
                self.urls[genre][title]['rate'] = rate

                try:
                    temp_count = elem.find_element_by_css_selector('.review_desc').text
                    count = re.sub(r'[^0-9]', '', temp_count)
                    self.urls[genre][title]['count'] = count
                except: pass
                    
            tqdm_pages.set_description(genre+' '+str(page)+' urls')
        tqdm_pages.close()

    def connect_mysql(self, local=True, connect=True): # mysql과 연결(DataBase: pagepalette)
        if connect:
            if local: # 실행 서버가 local인 경우
                host, user, pw = 'localhost', 'root', '1234'
            else: # 실행 서버가 원격인 경우
                host, user, pw = '192.168.0.176', 'pagepalette', 'pagepalette0528'
            self.db = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db='pagepalette', 
                                      charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
        else:
            self.db.commit()
            self.db.close
            
    def create_tbl(self, genre): # mysql table 생성
        self.connect_mysql(False, True)
        sql = """CREATE TABLE IF NOT EXISTS gyobo_{}(
                title VARCHAR(100), author VARCHAR(100),
                large_category VARCHAR(200), middle_category VARCHAR(300), 
                b_rank SMALLINT, rate DOUBLE, count SMALLINT, isbn BIGINT, img VARCHAR(300)
                );""".format(genre)
        self.cursor.execute(sql)
        self.connect_mysql(False, False)
    
    def fill_tbl(self, genre): # url정보로 mysql table 채우기
        self.connect_mysql(False, True)
        tqdm_book = tqdm(self.urls[genre].items())
        for book_title, book_info in tqdm_book:
            try: self.open_driver(book_info['url'], scroll=True)
            except: continue
                
            title = book_title
            author, rank = book_info['author'], book_info['rank']
            rate = book_info['rate']
            count = book_info['count'] if book_info['count'] is not None else 'Null'
            
            elems = self.driver.find_elements_by_class_name('category_list_item')
            genre_1, genre_2 = '', ''
            for elem in elems:
                gs = elem.find_elements_by_class_name('intro_category_link')
                for i, g in enumerate(gs):
                    if i==1: genre_1 += g.text+', '
                    elif i==2 or i==3: genre_2 += g.text+', '
            if len(genre_1)==0: continue
                        
            isbn_box = self.driver.find_element_by_class_name('product_detail_area.basic_info')
            isbn = int(isbn_box.find_element(By.TAG_NAME, 'td').text)
            
            try:
                img_box = self.driver.find_element_by_class_name('portrait_img_box.portrait')
                img = img_box.find_element(By.TAG_NAME, 'img').get_attribute('src')
            except: img = 'Null'
            
            sql = '''INSERT INTO gyobo_{0} VALUES(
            "{1}", "{2}", "{3}", "{4}", {5}, {6}, {7}, {8}, "{9}");
            '''.format(genre, title, author, genre_1, genre_2, rank, rate, count, isbn, img)
            self.cursor.execute(sql)
            self.db.commit()
            tqdm_book.set_description(genre+' insert data')
        self.connect_mysql(False, False)
        tqdm_book.close()
        
    def get_df(self, genre): # mysql에 생성된 table을 dataframe으로 불러와 csv파일로 저장하기
        self.connect_mysql(True)
        sql = 'SELECT * FROM gyobo_{}'.format(genre)
        self.cursor.execute(sql)
        self.dfs[genre] = pd.DataFrame(self.cursor.fetchall())
        self.dfs[genre].to_csv('gyobo_{}.csv'.format(genre), index=False)
        self.connect_mysql(False)
        print('save gyobo_'+genre+'.csv')
    
    def auto(self, genre, opt=True): # 모든 과정 한 번에 실행
        if opt: self.save_urls(genre)
        self.create_tbl(genre)
        self.fill_tbl(genre)
        self.get_df(genre)