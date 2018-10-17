from bottledaemon import daemon_run
from bottle import route, run 
import sqlite3
import json
import email
import smtplib
from bottle import hook, response
from bottle import get, post, request
from bottle import route, run 
import logging
import os
import sys

# __name__はこのモジュールの名前
logger = logging.getLogger(__name__)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route("/hello")
def hello():
   return "Hello World"
 
@route('/search', method='GET')
def search():
    datas = []
    keyword = request.query.keyword
    print(keyword)
    datas = query_db("/opt/api/info.db", 'select * from human where name LIKE ?',('%{}%'.format(str(keyword)),))

    result = {'datas': []}
    result_title = result['datas']

    for d in datas:
        result_title.append({
            "id": d.get('id'),
            "name": d.get('name'),
            "part": d.get('part'),
            "position": d.get('position'),
            "mail": d.get('mail'),
            "etc": d.get('etc')
        })

    return result

# @route('/upload', method='POST')
# def upload():
#     upload = request.files.query('upload')
#     print(upload)
#     sys.stdout.write(bottle.request.files.get('upload').filename);
#     name, ext = os.path.splitext(upload.filename)
#     print(name)
#     print(ext)
#     inputfile = open('/opt/api/img/%s'%upload.filename, 'wb')
#     inputfile.write(upload.file.read())
#     inputfile.close()
#     return 'OK'

#File Upload
@get('/upload')
def upload():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="submit" value="Upload"></br>
            <input type="file" name="upload"></br>
        </form>
    '''

@route('/upload', method='POST')
def do_upload():
    # upload = request.files.get('upload', '')
    upload = request.files.get('upload', '')
    print("*************")
    if upload is None:
        print("null")
    else:
        print(upload)
        print("*************")
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    # save_path = get_save_path()
    upload.save("/opt/img/")
    return 'Upload OK. FilePath: %s%s' % ("/opt/img/", upload.filename)

@route('/email', method='GET')
def email_send():
    print(request.query.title)
    print(request.query.email)
    print(request.query.sub)
    logger.debug("test")
    to = 'starful@starful.net'
    fromMy  = 'starful0418@gmail.com'
    subj='TheSubject'
    date='13/8/2018'
    message_text='Hello Or any thing you want to send'
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )

    username = str('starful0418@gmail.com')
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

def query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
    except sqlite3.Error as e:
        print('query_db : sqlite3.Error occurred:' + str(e.args[0]))
    return (r[0] if r else None) if one else r

if __name__ == "__main__":
  # daemon_run(host='0.0.0.0', port=99)
  run(host='0.0.0.0', port=99)  