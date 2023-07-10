import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from .models import Female10,Female20,Female30,Female40,Female50,Female60
# from .models import Male10,Male20,Male30,Male40,Male50,Male60
from .models import Gyobo,Gyobo01,Gyobo03,Gyobo05,Gyobo13
from .models import Gyobo15,Gyobo17,Gyobo19,Gyobo23,Gyobo29

class sortBook():  # 사용자가 선택한 'middle_category'로 책 추천 후보 12권 select
    def __init__(self, user_info):
        self.models = {'소설': Gyobo01, '시에세이': Gyobo03, '인문': Gyobo05,
                       '경제경영': Gyobo13, '자기계발': Gyobo15, '정치사회': Gyobo17,
                       '역사문화': Gyobo19, '예술대중문화': Gyobo23,
                       '과학': Gyobo29, '기타': Gyobo}

        g1s = user_info['large_category'].values[0].split(',')
        g2s = user_info['middle_category'].values[0].split(',')
        self.genres = {g1: {'df': self.call_df(g1)} for g1 in g1s}
        for g1, g2 in zip(g1s, g2s):
            self.genres[g1][g2] = {}
        self.recomm1_books = self.__call__()

    def call_df(self, g1):  # 중복되는 데이터 또는 null값이 있는 행 제외하고 book df 불러오기
        books_queryset = self.models[g1].objects.all()
        df = pd.DataFrame.from_records(books_queryset.values('title','author', 'b_rank', 'count', 'img', 'isbn', 'large_category', 'middle_category', 'rate'))

        df.drop_duplicates(subset=['title', 'author'], ignore_index=True, inplace=True)
        return df.dropna()

    def recomm1_rank(self, g1, g2, n=240, check=True):  # 인기순으로 추천
        df = self.genres[g1]['df'].copy()

        try:
            idx = df[df['middle_category'] == g2].index.values[0]
        except:
            check = False
            df = pd.concat([df, pd.DataFrame({'middle_category': [g2]})], ignore_index=True)
            idx = df[df['middle_category'] == g2].index.values

        cvect = CountVectorizer(ngram_range=(1, 3))
        cvect_g2 = cvect.fit_transform(df['middle_category'])
        csim_g2 = cosine_similarity(cvect_g2, cvect_g2).argsort()[:, ::-1]

        sim_idx = csim_g2[idx, :n].reshape(-1)
        sim_idx = sim_idx if check else sim_idx[sim_idx != idx]
        self.genres[g1][g2]['df'] = df.iloc[sim_idx].sort_values(['b_rank', 'rate'], ascending=[True, False])

    def __call__(self):  # 선택한 장르마다 책을 추천해 총 12권의 추천목록 반환
        order_li = ['A','B','C','D']
        select_dfs, i = [], 0
        g1_n, g1_c = 480 // len(self.genres.keys()), 12 // len(self.genres.keys())
        for g1, g2s in self.genres.items():
            g2_n, g2_c = g1_n // (len(g2s.keys()) - 1), g1_c // (len(g2s.keys()) - 1)
            for g2 in g2s.keys():
                if g2 == 'df': continue
                self.recomm1_rank(g1, g2, g2_n)
                df = self.genres[g1][g2]['df'].reset_index(drop=True)
                idxs = []
                while len(idxs)<g2_c:
                    idx = np.random.randint(30)
                    if idx not in idxs:
                        idxs.append(idx)
                df = df.loc[idxs]
                df = pd.concat([df.reset_index(drop=True), pd.DataFrame({'order': [order_li[i] for j in range(len(df))]})],
                               axis=1)
                i += 1
                select_dfs.append(df)
        result_df = pd.concat(select_dfs, axis=0)
        return result_df