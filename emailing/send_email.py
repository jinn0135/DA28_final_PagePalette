import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import pymysql
import pickle
from recommBook import sortBook, recommBook

# 뉴스 클리핑 부분
class News():
    def __init__(self, date, reception_time):
        self.date = date
        self.time = 'pm' if reception_time else 'am'
    def __call__(self, opt='news'):        
        file = 'news_form.html' if opt=='news' else 'newsbooks_form.html'
        with open(file, 'r', encoding='UTF8') as f:
            news_html = f.read()
            
        news_df = pd.read_csv('{}_{}.csv'.format(self.date, self.time))
        topics = news_df['topic'].unique().tolist()
        for i,topic in enumerate(topics):
            sub_df = news_df[news_df['topic']==topic]
            wc = sub_df['wc'].values[0]
            news_html = news_html.replace('토픽{}_키워드'.format(i+1), topic)
            news_html = news_html.replace('토픽{}_wc'.format(i+1), wc)
            for j, row in enumerate(sub_df.itertuples()):
                news_html = news_html.replace('토픽{}_제목{}'.format(i+1,j+1), row.title)
                news_html = news_html.replace('토픽{}_링크{}'.format(i+1,j+1), row.link)
                news_html = news_html.replace('토픽{}_요약{}'.format(i+1,j+1), row.desc)
        return news_html
    
# 도서 추천 부분
class Books():
    def __init__(self, html, user_info):
        self.html, self.user_info = html, user_info
        
    def __call__(self):
        userRecomm = recommBook(self.user_info)
        books_df = userRecomm()
        params = {'제목':'title', '저자':'author', '링크':'url', '이미지':'img'}
        
        for i in range(len(books_df)):
            for p, col in params.items():
                val = books_df.loc[i, col]
                self.html = self.html.replace('책{}_{}'.format(i+1, p), val)
        return self.html
    
#메일 보내기
class sendEmail():
    def __init__(self, user_df=None):
        if user_df is None:
            self.users_opt = self.get_table('user_option')
        else: self.users_opt = user_df
        self.bookservice = None
        self.now = datetime.now()
        self.reception_time = 1
        self.email_id, self.email_pw = 'pagepallete', 'hwbj ofvz difa uewj'

# DB연결
    def connect_mysql(self, local=True, connect=True):
        if connect:
            if local:
                host, user, pw, db = 'localhost', 'root', '1234', 'example'
            else:
                host, user, pw, db = '192.168.0.176', 'pagepalette', 'pagepalette0528', 'pagepalette'
            self.db = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=db, 
                                      charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
        else:
            self.db.commit()
            self.db.close

# 유저 정보 불러오기
    def get_table(self, table_name):
        self.connect_mysql(local=False, connect=True)
        sql = 'SELECT * FROM {}'.format(table_name) # user_option table
        self.cursor.execute(sql)
        df = pd.DataFrame(self.cursor.fetchall())
        self.connect_mysql(local=False, connect=False)
        return df

# 사용자가 지정한 시간과 날짜에 맞게 이메일 보낼 수 있도록 설정
    def user_select(self):
        if self.now.hour in range(0,7) or self.now.hour in range(17,24):
            self.users_opt = self.users_opt[self.users_opt['reception_time']==0]
            self.reception_time = 0
        else: self.users_opt = self.users_opt[self.users_opt['reception_time']==1]
        
        if self.now.weekday()==2: # 금
            if 'large_category' in self.users_opt.columns:
                self.bookservice = self.users_opt[self.users_opt['book_service']==1]
            else:
                book_user = self.users_opt.loc[self.users_opt['book_service']==1,'email']
                user_info_df = self.get_table('user_info')
                book_option_df = self.get_table('book_option')
                book_user = book_user.merge(user_info_df, how='left', on='email')
                self.bookservice = book_user.merge(bookservice_df, how='left', on='email')
            self.users_opt = self.users_opt[self.users_opt['book_service']==0]
        elif self.now.weekday() in [5,6]: # 토,일
            self.users_opt = self.users_opt[self.users_opt['weekend']==1]
        
# 뉴스서비스만 신청한 사용자는 뉴스만, 뉴스와 도서서비스 모두 신청한 사용자는 둘 다 전송될 수 있게 설정
    def content_msg(self, user_info=None, opt='news'):
        if opt=='news':
            news = News(str(self.now.date()), self.reception_time)
            return news(opt)
        else: # opt='newsbooks'
            news = News(str(self.now.date()), self.reception_time)
            html = news(opt)
            books = Books(html, user_info)
            return books()
    
    def write_email(self, book_service=False):
        if book_service:
            message_To = self.bookservice['email'].tolist()
            for user_email in message_To:
                user_info = self.bookservice[self.bookservice['email']==user_email]
                content = self.content_msg(user_info, opt='newsbooks')
                self.send_email(content, user_email)
        else: 
            content = self.content_msg()
            message_To = self.users_opt['email'].tolist()
            self.send_email(content, message_To)
        print('{} 메일발송 완료'.format('news & books' if book_service else 'news'))
        
    def send_email(self, content, message_To):
        # message에 수신자, 발신자, 메일내용 담기
        content = content.replace('날짜', str(self.now.date()))
        message = MIMEMultipart()
        message['Subject'] = '{}:{} Page Palette test mail'.format(self.now.hour, self.now.minute)
        message['From'] = "pagepallete@gmail.com"
        mimetext = MIMEText(_text=content, _subtype='html', _charset='utf-8')
        message.attach(mimetext)

        # smtp 이용해서 메일 발송
        smtp = smtplib.SMTP('smtp.gmail.com', 587) # TLS: 587 / SSL: 465
        smtp.ehlo()
        smtp.starttls() # TLS 이용
        smtp.login(self.email_id, self.email_pw) # 로그인 후 메일발송
        smtp.sendmail(message['From'], message_To, message.as_string())
        smtp.quit()
    
    def __call__(self):
        self.user_select() # user가 선택한 option에 따라 발송대상 선택
        if len(self.users_opt)!=0:
            self.write_email() # 뉴스만 전송받는 대상자가 한 명이라도 있으면 발송
        if self.bookservice is not None:
            self.write_email(book_service=True) # 뉴스&책 발송받는 대상이 있으면 발송
            
class RunService(): # 이메일 발송 서비스 실행
    def __init__(self):
        self.user_df = pd.DataFrame({
            'email':['tutujin007@naver.com','tutujin3129@gmail.com',
                     'pagepallete@gmail.com','kyooon6248@naver.com',
                     'qkrdbdud98@naver.com'],
            'gender':['female','female','female','female','female'], 
            'age':[20,20,20,20,20],
            'reception_time':[0 for i in range(5)], 'weekend':[1 for i in range(5)],
            'book_service':[0,1,0,1,1],
            'large_category':[None,'소설,소설,시에세이',None,
                              '소설,인문','예술대중문화,예술대중문화'],
            'middle_category':[None,'영미소설,판타지소설,한국시',None,
                               '한국소설,철학','영화,음악'],
            'selected_book_isbn':[None,'9788925554990,9788925576633,9791157956357',None,
                                  '9791191891287,9788937834790','9788934942436,9788967212032']
            })
    def __call__(self, opt='service'):
        if opt=='demo': # self.user_df 정보로만 이메일 전송
            send_mail = sendEmail(self.user_df)
        else: # mysql의 DataBase 정보로 이메일 발송
            send_mail = sendEmail()
        send_mail()