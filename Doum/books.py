import random
import pandas as pd
import numpy as np
import shutil, os

class Books:
    DEPARTMENTS = ('인문대학', '공과대학', '자연과학', '사회과학', '의과대학')
    SUBJECTS = ('사회탐구', '과학탐구', '국어', '수학', '영어')

    def __init__(self, csv_path: str):
        dir = 'backup'
        os.makedirs(dir, exist_ok=True)
        self.csv_path = csv_path
        self.backup_csv_path = os.path.join(dir, self.csv_path)
        self.df = pd.read_csv(csv_path, encoding='euc-kr')
        self.df.replace({np.nan: ''}, inplace=True)

    def get_info(self, title):
        """
        Object 형태의 제목에 일치되는 책 정보 검색한다.
        일치된 항목이 있는 경우 다음과 같은 형식의 데이터를 반환한다.
        {'과목': '사회탐구', '제목': '나의 하루는 4시 30분에 시작된다', '키워드': '꿈,자기계발,자기개발,성공학,경영관리,시간관리,아침형,생활습관',
        '저자': '김유진 ', '출판사': '토네이도',
        '예스24': 'http://www.yes24.com/Product/Goods/93513663',
        '교보': 'http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&linkClass=&barcode=9791158511906 ',
        '알라딘': 'https://www.aladin.co.kr/shop/wproduct.aspx?ISBN=K922633306&start=pnaver_02 ', '이미지': None,
        '인문대학': 0, '공과대학': 0, '자연과학': 0, '사회과학': 0, '의과대학': 0,
        '인문대학N': 1, '공과대학N': 1, '자연과학N': 1, '사회과학N': 1, '의과대학N': 1}
        """
        df2 = self.df.query(f'title == "{title}"')
        obj_list = df2.to_dict('records') 
        if len(obj_list) > 0:
            return obj_list[0]

    # 특정 학과에 적합한 가장 높은 점수순으로 책을 n개 반환한다.
    def suggest_top_books(self, department, subject, n, random_count):
        # 특정 과목의 책들만 선정
        df2 = self.df.query(f'subject == "{subject}"')
        # 선정된 책들중 평점이 높은 순으로 배열
        df3 = df2.sort_values(by=[department], ascending=False)
        books = []
        for idx, row in df3.iterrows():
            title = row['title']
            print('ranking:', idx, title)
            info = self.get_info(title)
            #print(f'suggest_top_books idx={idx} title={title} -> {info}')
            books.append(info)
        selected = books[:n]   # 최종적으로 n개만 빼내어 반환
        if len(books) > n and random_count > 0:
            selected += random.sample(books[n:], random_count)
        return selected

    def update_this_department_book_score(self, department, book_title, score):
        df2 = self.df.query(f'title == "{book_title}"')
        department_n = department + 'N'
        row_idx = df2.index[0]
        cur_score = self.df.at[row_idx, department]
        print(f'row_idx={row_idx} department={department} cur_score={cur_score}')
        num_score = self.df.at[row_idx, department_n]
        new_score = (cur_score * num_score + score) / (num_score + 1)
        print(f'{book_title} ({cur_score} * {num_score} + {score}) / ({num_score} + 1) = {new_score}')
        self.df.at[row_idx, department] = new_score
        self.df.at[row_idx, department_n] = num_score + 1

    def euclidean_distance(self, data, name1, name2):
        sum=0
        # for i in data[name1]:
        #     if i in data[name2]: # 같은 책을 봤다면
        #         sum+=math.pow(data[name1][i]- data[name2][i],2)
        # return 1/(1+math.sqrt(sum))

    def save_to_csv(self):
        shutil.move(self.csv_path, self.backup_csv_path)
        self.df.to_csv(self.csv_path, encoding='euc-kr', index=False)
        print(f'save to {self.csv_path}')
