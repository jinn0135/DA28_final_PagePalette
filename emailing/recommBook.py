import numpy as np
import pandas as pd
import pymysql
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote


class sortBook(): # 사용자가 선택한 선호장르를 바탕으로 책 추천 후보 12권 select
    def __init__(self, user_info):
        g1s = user_info['large_category'].values[0].split(',')
        g2s = user_info['middle_category'].values[0].split(',')
        self.genres = {g1:{'df':self.call_df(g1)} for g1 in g1s}
        for g1,g2 in zip(g1s, g2s):
            self.genres[g1][g2] = {}
        self.recomm1_books = self.__call__()
        
    def connect_mysql(self, local=True, connect=True): # mysql과 연결
        if connect:
            if local: # local 서버를 사용할 경우
                host, user, pw, db = 'localhost', 'root', '1234', 'example'
            else: # 서버에 원격으로 접속할 경우
                host, user, pw, db = '192.168.0.176', 'pagepalette', 'pagepalette0528', 'pagepalette'
            self.db = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=db, 
                                      charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
        else:
            self.db.commit()
            self.db.close
    
    def call_df(self, g1): # 중복되는 데이터 또는 null값이 있는 행 제외하고 book df 불러오기
        self.connect_mysql(local=True, connect=True)
        sql = 'SELECT * FROM gyobo_{}'.format(g1)
        self.cursor.execute(sql)
        df = pd.DataFrame(self.cursor.fetchall())
        self.connect_mysql(local=True, connect=False)
        
        df.drop_duplicates(subset=['title','author'], ignore_index=True, inplace=True)
        return df.dropna()
    
    def recomm1_rank(self, g1, g2, n=240, check=True): # 인기순으로 추천
        df = self.genres[g1]['df'].copy()
        
        try: idx = df[df['middle_category']==g2].index.values[0]
        except:
            check = False
            df = pd.concat([df, pd.DataFrame({'middle_category':[g2]})], ignore_index=True)
            idx = df[df['middle_category']==g2].index.values

        cvect = CountVectorizer(ngram_range=(1,3))
        cvect_g2 = cvect.fit_transform(df['middle_category'])
        csim_g2 = cosine_similarity(cvect_g2, cvect_g2).argsort()[:,::-1]
        
        sim_idx = csim_g2[idx, :n].reshape(-1)
        sim_idx = sim_idx if check else sim_idx[sim_idx != idx]
        self.genres[g1][g2]['df'] = df.iloc[sim_idx].sort_values(['b_rank','rate'], ascending=[True, False])
    
    def __call__(self): # 선택한 장르마다 책을 추천해 총 12권의 추천목록 반환
        order_li = ['A','B','C','D']
        select_dfs, i = [], 0
        g1_n, g1_c = 480//len(self.genres.keys()), 12//len(self.genres.keys())
        for g1, g2s in self.genres.items():
            g2_n, g2_c = g1_n//(len(g2s.keys())-1), g1_c//(len(g2s.keys())-1)
            for g2 in g2s.keys():
                if g2=='df': continue
                self.recomm1_rank(g1, g2, g2_n)
                df = self.genres[g1][g2]['df'].reset_index(drop=True)
                idxs = []
                while len(idxs)<g2_c:
                    idx = np.random.randint(30)
                    if idx not in idxs:
                        idxs.append(idx)
                df = df.loc[idxs]
                df = pd.concat([df.reset_index(drop=True),pd.DataFrame({'order':[order_li[i] for j in range(len(df))]})], 
                               axis=1)
                i += 1
                select_dfs.append(df)
        result_df = pd.concat(select_dfs, axis=0)
        return result_df
    
class recommBook(): # 이메일로 보낼 추천도서목록
    def __init__(self, user_info):
        self.gender = user_info['gender'].values[0]
        self.age = user_info['age'].values[0]
        
        sort = sortBook(user_info) # 각 middle_category 마다의 상위 도서목록 가져오기
        g1s = user_info['large_category'].values[0].split(',')
        g2s = user_info['middle_category'].values[0].split(',')
        self.selected_n = len(g2s)
        selected_books = user_info['selected_book_isbn'].values[0].split(',')
        if self.selected_n==1:
            selected_books = [selected_books]
        else: selected_books = [[book] for book in selected_books]
            
        self.genres = {g1:{} for g1 in g1s}
        for g1,g2,isbn in zip(g1s,g2s,selected_books):
            self.genres[g1][g2] = {'isbn':isbn, 'df':sort.genres[g1][g2]['df']}
        self.df_ga = self.make_df_ga()
    
    def connect_mysql(self, local=True, connect=True): # mysql 연결
        if connect:
            if local: # local
                host, user, pw, db = 'localhost', 'root', '1234', 'example'
            else: # 원격서버
                host, user, pw, db = '192.168.0.176', 'pagepalette', 'pagepalette0528', 'pagepalette'
            self.db = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=db, 
                                      charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
        else:
            self.db.commit()
            self.db.close
    
    def make_df_ga(self): # mysql에서 gender&age에 따른 인기도서목록 가져오기
        self.connect_mysql(local=True, connect=True)
        sql = 'SELECT * FROM {}_{}'.format(self.gender, self.age)
        self.cursor.execute(sql)
        df = pd.DataFrame(self.cursor.fetchall())
        self.connect_mysql(local=True, connect=False)
        return df
    
    def recomm2_rate(self, g1, g2, selected_isbn): # 평점기준 추천목록 작성
        df = self.genres[g1][g2]['df'].copy().reset_index(drop=True)
        n = len(df)//2
        
        cvect = CountVectorizer(ngram_range=(1,3))
        cvect_g2 = cvect.fit_transform(df['middle_category'])
        csim_g2 = cosine_similarity(cvect_g2, cvect_g2).argsort()[:,::-1]

        idx = df[df['isbn'] == float(selected_isbn)].index.values
        sim_idx = csim_g2[idx, :n].reshape(-1)
        sim_idx = sim_idx[sim_idx != idx]
        return df.iloc[sim_idx].sort_values(['b_rank', 'rate'], ascending=[True, False])
    
    def recomm2_ga(self, g1, g2, selected_isbn): # 성별,연령별 추천목록과 평점기준 정렬과 합치기
        df = self.recomm2_rate(g1, g2, selected_isbn)
        df_ga = pd.merge(self.genres[g1][g2]['df'], self.df_ga, how='inner', 
                         left_on='isbn', right_on='agender_isbn')[['agender_rank','agender_isbn']]
        
        bins, labels = [i for i in range(0,210,10)], [i for i in range(-200, 0, 10)]
        df_ga['ga_new_rank'] = pd.cut(df_ga['agender_rank'], bins=bins, labels=labels)
        new_df = pd.merge(df, df_ga, how='left', left_on='isbn', right_on='agender_isbn').drop(columns=['agender_isbn'])
        new_df['ga_new_rank'] = new_df['ga_new_rank'].astype({'ga_new_rank':float})
        new_df['ga_new_rank'] = new_df['ga_new_rank'].fillna(0)
        new_df['new_rank'] = new_df['b_rank'] + new_df['ga_new_rank']
        return new_df.sort_values(['new_rank','rate'], ascending=[True, False])
    
    def __call__(self): # 총 4권의 추천도서목록 결정
        result_li, i = [], 0
        for g1, g2s in self.genres.items():
            for g2 in g2s.keys():
                if g2=='df': continue
                for selected_isbn in self.genres[g1][g2]['isbn']:
                    author = self.genres[g1][g2]['df'].loc[self.genres[g1][g2]['df']['isbn']==selected_isbn, 'author']
                    author_df = self.genres[g1][g2]['df'][self.genres[g1][g2]['df']['author']=='author']
                    df = pd.concat([self.recomm2_ga(g1, g2, selected_isbn).iloc[:50,:], author_df], axis=0)
                    df.drop_duplicates(subset=['title','author'], ignore_index=True, inplace=True)
                    if self.selected_n<=2 or(self.selected_n==3 and i==0):
                        recomm_n = 2
                    else:recomm_n = 1
                    i += 1
                    idxs = []
                    while len(idxs)<recomm_n:
                        idx = np.random.randint(30)
                        if idx not in idxs:
                            idxs.append(idx)
                    result_li.append(df.loc[idxs])
        result_df = pd.concat(result_li, axis=0).reset_index(drop=True)
        result_df['url'] = result_df['title'].apply(lambda x: 'https://www.google.com/search?tbm=bks&q={}'.format(quote(x)))
        return result_df[['title','author','img','url']] # 이메일에 보내줄 정보들만 반환