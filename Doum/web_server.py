from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from recommendation import *
from books import Books

app = Flask(__name__)
books_ = Books('books.csv')

department_map = {
    '1': '자연과학계열',
    '2': '의약계열',
    '3': '공학계열',
}

@app.route("/")
def index():
    """ index.html 파일을 브라우저에게 제공한다. """
    #return send_from_directory('.', 'index.html')
    return redirect(url_for('page1'))

@app.route("/index.js")
def index_js():
    """ index.js 파일을 브라우저에게 제공한다. """
    return send_from_directory('.', 'index.js')

@app.route("/test.html")
def test_html():
    """ test.html 파일을 브라우저에게 제공한다. """
    return send_from_directory('.', 'test.html')

@app.route("/bootstrap.min.css")
def bootstrap_css():
    """ bootstrap.min.css 파일을 브라우저에게 제공한다. """
    return send_from_directory('.', 'bootstrap.min.css')

@app.route("/page1/")
def page1():
    """ page1 파일을 브라우저에게 제공한다. """
    # 램덤하게 두개의 학과를 선택
    # department = random.choice(books_.DEPARTMENTS)
    # subjects = random.sample(books_.SUBJECTS, 2)
    # books0 = books_.suggest_top_books(department, subjects[0], 5, 0)
    # books1 = books_.suggest_top_books(department, subjects[1], 5, 0)
    # return render_template('page1.html', department=department, subject0=subjects[0], books0=books0, subject1=subjects[1], books1=books1)
    return render_template('page1.html')

@app.route("/page2/")
def page2():
    """ page2 파일을 브라우저에게 제공한다. """
    return render_template('page2.html')

@app.route("/page3/<department>")
def page3(department):
    """ page3 파일을 브라우저에게 제공한다. """
    department_name = department_map[department]
    return render_template('page3.html', department=department,
         department_name=department_name)

@app.route("/page4/<department>/<subject>")
def page4(department, subject):
    """ page4 파일을 브라우저에게 제공한다. """
    return render_template('page4.html', department=department,
         subject=subject)

@app.route("/page5/<department>/<subject>/<book>/")
def page5(department, subject, book):
    """ page5 파일을 브라우저에게 제공한다. """
    return render_template('page5.html', department=department,subject=subject,book=book)

@app.route("/page5-answer/<department>/<subject>/<book>/<score>")
def page5_answer(department, subject, book, score):
    """ page5 파일을 브라우저에게 제공한다. """
    score = float(score)
    books_.update_this_department_book_score(department, book, score)
    # for each_department in Books.DEPARTMENTS:
    #     if department != each_department:
    #         sim_value = euclidean_distance(mapping_table, department, each_department)
    #         #print(f'each_department={each_department} sim_value={sim_value}')
    #         update_other_department_book_score(each_department, book, score, sim_value)
    books_.save_to_csv()
    return redirect(url_for('index'))

@app.route("/page6/<subject>")
def page6(subject):
    """ page6 파일을 브라우저에게 제공한다. """
    if subject == '없음':
        subject = random.choice(books_.SUBJECTS)
    if subject == '과학':
        subject = '과학탐구'
        page_name = 'page6-science.html'
        department = '자연과학'
    elif subject == '국어':
        page_name = 'page6-language.html'
        department = '인문대학'
    elif subject == '사회':
        subject = '사회탐구'
        page_name = 'page6-society.html'
        department = '사회과학'
    elif subject == '영어':
        page_name = 'page6-english.html'
        department = '인문대학'
    else:  #subject == '수학':
        page_name = 'page6-math.html'
        department = '공과대학'
    books = books_.suggest_top_books(department, subject, 3, 1)
    #print(f'page4: department={department} --> {books}')
    for i in range(100):
        subject1 = random.choice(books_.SUBJECTS)
        if subject1 != subject:
            break
    books0 = books_.suggest_top_books(department, subject, 5, 0)
    print(f'books={books0}')
    books1 = books_.suggest_top_books(department, subject1, 5, 0)
    return render_template(page_name, subject0=subject, books0=books0, subject1=subject1, books1=books1)

@app.route("/page7/<page_html>")
def page7(page_html):
    return render_template(page_html)

@app.route("/scores.html")
def scores_html():
    """ scores.html 파일을 브라우저에게 제공한다. """
    return send_from_directory('.', 'scores.html')

@app.route("/books.csv")
def books_csv():
    return send_from_directory('.', 'books.csv')

@app.route("/recommend-books/<department>")
def recommend_books(department):
    """ 책을 추천한다. """
    books = suggest_top_books(department, 3)
    print('추천 도서:', books)
    random_book = suggest_random_book(department, books)
    books.append(random_book)
    #print(f'recommend_books: department={department} --> {books}')
    return { 'books':  books }
    #return { 'books': ['인터스텔라의 과학', '미적분으로 바라본 하루', '노인과 바다'] }

@app.route("/book-score", methods = ['POST'])
def book_score():
    """ 사용자의 평점을 해당 책의 랭킹 점수에 반영한다. """
    data = request.json
    print(f'book-score: data={data}')
    department = data['department']
    book = data['book']
    score = data['score']
    update_this_department_book_score(department, book, score)
    for each_department in mapping_table.keys():
        if department != each_department:
            sim_value = euclidean_distance(mapping_table, department, each_department)
            #print(f'each_department={each_department} sim_value={sim_value}')
            update_other_department_book_score(each_department, book, score, sim_value)
    return { 'result':  0 }

@app.route("/score-table")
def score_table():
    """ 전체 매핑 테이블 내용을 반환한다. """
    return { 'mapping_table':  mapping_table }

@app.route("/hello")
def hello():
    return '''
<html>
   <head>
      <title>HTML Backgorund Color</title>
   </head>
   <body style="background-color:lightgreen;">
      <h1>Products</h1>
      <p>We have developed more than 10 products till now.</p>
   </body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
