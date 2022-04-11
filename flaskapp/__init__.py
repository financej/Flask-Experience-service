from flask import Flask, g, request, Response, make_response, session, render_template, Markup
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True  # use only debug
# app.jinja_env.trim_blocks = True

app.config.update(
    SECRET_KEY="X1234xRH!mHwf",
    SESSION_COOKIE_NAME="flask_session",
    PERMANENT_SESSION_LIFETIME=timedelta(31)  # 31days
)


@app.route('/')
def idx():
    return render_template('app.html', ttt='test111')


@app.route('/top100')
def top100():
    return render_template('application.html')


@app.route('/main')
def main():
    return render_template('main.html', title="main title")


@app.route('/tmpl2')
def tmpl2():
    a = (1, "만남1", "김건모", False, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "익명", False, [a, b])
    d = (4, "만남4", "익명", False, [a, b, c])

    return render_template("index.html", lst2=[a, b, c, d])


class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children


@app.route('/tmpl3')
def tmpl3():
    py = Nav("파이썬", "https://search.naver.com")
    java = Nav("자바", "https://search.naver.com")
    t_prg = Nav("프로그래밍 언어", "https://search.naver.com", [py, java])

    jinja = Nav("Jinja", "https://search.naver.com")
    gc = Nav("Genshi, Cheetah", "https://search.naver.com")
    flask = Nav("플라스크", "https://search.naver.com", [jinja, gc])

    spr = Nav("스프링", "https://search.naver.com")
    ndjs = Nav("노드JS", "https://search.naver.com")
    t_webf = Nav("웹 프레임워크", "https://search.naver.com", [flask, spr, ndjs])

    my = Nav("나의 일상", "https://search.naver.com")
    issue = Nav("이슈게시판", "https://search.naver.com")
    t_others = Nav("기타", "https://search.naver.com", [my, issue])

    return render_template("index.html", navs=[t_prg, t_webf, t_others])


@app.route("/tmpl/")
def tmpl():
    tit = Markup("<strong>Title</strong>")
    print(">>>>>", type(tit))
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)
    lst = [(1, "만남", "김건모", False), (2, "만남", "노사연", True), (3, "만남", "익명", False)]
    return render_template('index.html', title=tit, mu=h, lst=lst)


# app.config['SERVER_NAME'] = 'local.com:5000'
#
# @app.route("/sd", subdomain="g")
# def helloworld_sub_local():
#     return "Hello g.local.com"

# @app.route('/setsess')
# def setsess():
#     session['Token'] = '123X'
#     return "Session이 설정되었습니다!"
#
# @app.route('/getsess')
# def getsess():
#     return session.get('Token')

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다."


@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session['Token'] = '123X'
    return make_response(res)


@app.route('/rc')
def rc():
    key = request.args.get('key')  # token
    val = request.cookies.get(key)
    return "cookie[" + key + "] = " + val + " , " + session.get('Token')


@app.route("/reqenv")
def reqenv():
    return (
               'REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
               'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
               'PATH_INFO: %(PATH_INFO) s <br>'
               'QUERY_STRING: %(QUERY_STRING) s <br>'
               'SERVER_NAME: %(SERVER_NAME) s <br>'
               'SERVER_PORT: %(SERVER_PORT) s <br>'
               'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
               'wsgi.version: %(wsgi.version) s <br>'
               'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
               'wsgi.input: %(wsgi.input) s <br>'
               'wsgi.errors: %(wsgi.errors) s <br>'
               'wsgi.multithread: %(wsgi.multithread) s <br>'
               'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
               'wsgi.run_once: %(wsgi.run_once) s') % request.environ


# request 처리용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)

    return trans


@app.route("/dt")
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식 : " + str(datestr)


@app.route("/sd")
def helloworld_local():
    return "Hello Local.com"


@app.route("/res1")
def res1():
    # response_class
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)


# str : Simple String (HTML, JSON)
# return make_response("custom response")

@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = "the request method was %s" % environ["REQUEST_METHOD"]
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


# 리스폰가 다 나가고 난뒤 실행 - destroy
# @app.teardown_request
#   def ... (exception)
# appcontext가 다 끝난뒤 실행 - destroy
# @app.teardown_appcontext
#  def ... (exception)

@app.route('/rp')
def rp():
    q1 = request.args.get('q')
    q2 = request.args.getlist('q')
    return "q = %s" % str(q2)


# http://localhost:5000/rp?q=123&q=English

# 리퀘스트를 처리하기전에 먼저 처리하라는 의미 - Web Filter
@app.before_request
def before_request():
    print("before request!!!")
    g.str = "한글"


#
# uri 부분
@app.route("/gg")
def helloworld2():
    return "Hello World" + getattr(g, 'str', '111')


@app.route("/hello")
def helloworld():
    return "Hello Flask World"
