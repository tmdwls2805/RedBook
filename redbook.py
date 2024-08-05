from flask import Flask, render_template, request, send_from_directory, jsonify, json
from module import dbModule
from pprint import pprint
from jinja2 import UndefinedError

app = Flask(__name__, static_url_path="/templates")         # html 루트 경로

app.debug = True

@app.route("/<path:path>")
def serve_page(path):
    return send_from_directory('templates', path)


@app.route("/")                                              # 맨 처음 화면
def index():
    db_class = dbModule.Database()                           # mongoDB 호출
    results = db_class.recentCrawledBook()                   # 최근 크롤링된 도서 정보가져오는 함수 호출
    results = json.loads(results)                            # 함수 결과를 json형식으로 불러옴
    pprint(results)
    return render_template("index.html", json=results)     # json 변수에 결과값을 담아 index.html로 이동


@app.route("/search.html", methods=['post'])               # 도서 검색기능 post 통신
def search():
    db_class = dbModule.Database()
    results = db_class.find(request.form['keyword'])        # form 태그에서 넘어온 keyword로 find함수 실행
    try:
        results = json.loads(results)
        pprint(results)
        return render_template("search.html", json=results)# json 변수에 결과값을 담아 search.html로 이동
    except UndefinedError:                                  # 검색 결과가 없을때 예외처리
        return "검색어를 잘못 입력하셨습니다."

@app.route("/getSearchCount/<keyword>", methods=['get'])  # 도서 검색기능 ajax 방식
def getSearchCount(keyword):
    db_class = dbModule.Database()
    count = json.loads(db_class.getSearchCount(keyword))     # get방식으로 keyword를 받아 getSearchCount 함수 실행
    return jsonify(count)                                   # json형식으로 리턴

@app.route("/search/<keyword>/<page>", methods=['get'])   # 검색 결과 페이징 기능
def search_ajax(keyword, page):
    db_class = dbModule.Database()
    results = json.loads(db_class.find_ajax(keyword, page))  # get방식으로 keyword와 page를 받아 결과를 페이징함
    pprint(results)
    return jsonify(results)


@app.route("/interBook/<page>", methods=['get'])          # 국내도서 전체를 불러오는 기능
def interBook(page):                                        # get 방식으로 page를 받아 페이징을 함
    db_class = dbModule.Database()
    print(page)
    results = db_class.load(page)
    results = json.loads(results)
    pprint(results)
    return jsonify(results)

@app.route("/getCount", methods=['get'])                  # 국내도서 전체를 책 개수를 불러오는 기능
def getCount():
    db_class = dbModule.Database()
    count = json.loads(db_class.getCount())
    return jsonify(count)

@app.route("/interBookCategory.html?=category=<category>", methods=['get'])
def getBookCategory(category):
    return "interBookCategory.html?=category="+category

@app.route("/interBookCategory/<category>/<page>", methods=['get'])
def getBookWithCategory(category, page):
    db_class = dbModule.Database()
    results = db_class.getBookCategory(category, page)
    results = json.loads(results)
    return jsonify(results)

if __name__ == "__main__":
    app.run()
