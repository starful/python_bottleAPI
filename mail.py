from bottle import route, run 
# from bottle import post, get, put, delete, request, response
from bottledaemon import daemon_run
import sqlite3
import json
import email
import smtplib

@route('/checklogin')
def a_book():
    datas = []
    db_path = "todo.db"
    datas = query_db(db_path, 'select users,passwd from users')
    search = filter(lambda datas: datas['users'] == request.query.id and datas['passwd'] == request.query.pw, datas)

    obj = next(search, None)
    # https://bottlepy.org/docs/dev/tutorial.html#generating-content
    # returnする値が辞書（もしくはそのサブタイプ）場合、Bottoleが自動的にレスポンスヘッダにapplication/jsonを付けてくれる！
    if obj is not None:
        return { 'result' : True }
    else:
        response.status = 404 
        return { 'result' : False }

@route('/email')
def email_send():
    print(request.query.title)
    print(request.query.email)
    print(request.query.sub)

    to = 'starful@starful.net'
    fromMy  = 'starful0418@gmail.com'
    subj='TheSubject'
    date='13/8/2018'
    message_text='Hello Or any thing you want to send'
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )

    username = str('starful@gmail.com')
    password = str('7278hwan')
    try:
	    server = smtplib.SMTP("smtp.gmail.com",587)
	    server.ehlo()
	    server.starttls()
	    server.ehlo()
	    server.login(username,password)
	    server.sendmail(fromMy, to, msg)
	    server.quit()
	    print('ok the email has sent')
    except Exception as e:
    	print(str(e))

@route("/search")
def search():
    print("ser")
    datas = []
    db_path = "todo.db"
    datas = query_db(db_path, 'select * from users')

    # con = sqlite3.connect('./test.db')
    # cur = con.cursor()
     
    # sql = "select * from sample";
    # cur.execute(sql)
     
    # for row in datas:
    #     print(row[0], row[1])
    # result_list = []
    # for i in range(len(datas)):
    #     result_list.append({
    #      "users": datas[i].get("users"),
    #      "passwd": datas[i].get("passwd")
    #     })
    result = {"datas": datas}
    # con.close()
    # books.append(request.json)
    return result

# @put('/books/<id:int>')
# def update_book(id):
#     search = filter(lambda book: book['id'] == id, books)
#     obj = next(search, None)

#     if obj is not None:
#         index = books.index(obj)
#         books[index] = request.json
#         return request.json
#     else:
#         response.status = 404 
#         return {}

# @delete('/books/<id:int>')
# def update_book(id):
#     search = filter(lambda book: book['id'] == id, books)
#     obj = next(search, None)

#     if obj is not None:
#         index = books.index(obj)
#         del books[index]
#         return {}
#     else:
#         response.status = 404
#         return {}

def query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
    except sqlite3.Error as e:
        logging.error('query_db : sqlite3.Error occurred:' + str(e.args[0]))
    # except Exception as e:
    #   logging.error(traceback.format_exc())
    return (r[0] if r else None) if one else r

if __name__ == "__main__":
    daemon_run(host='0.0.0.0', port=98)
