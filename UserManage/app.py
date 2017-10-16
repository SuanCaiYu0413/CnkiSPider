# coding:utf-8

from MongoDB import DBConn
from flask import Flask,render_template,jsonify,request,redirect,url_for

app = Flask(__name__)
dbconn = DBConn()
dbconn.conn()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search_cache')
def search_cache():
    keyword = request.args.get('keyword')
    return jsonify(dbconn.find_cache(keyword))


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    result = dbconn.find_keyword(keyword)
    if result:
        return jsonify({"msg":"true","data":result})
    else:
        return jsonify({'msg':"false"})

@app.route('/insert_keyword',methods=['POST'])
def insert_keyword():
    keyword = request.form['keyword']
    if dbconn.insert_keyword(keyword):
        return jsonify({'msg':u'添加成功'})
    else:
        return jsonify({'msg':u'该关键词已在待爬取列表'})

@app.route('/list')
def list():
    keyword = request.args.get('keyword')
    pageindex = request.args.get('pageindex')
    pagesize = request.args.get('pagesize')
    pageindex = int(pageindex) if pageindex else 0
    pagesize = int(pagesize) if pagesize else 0
    if not keyword:
        return redirect('/')

    if (not pageindex) or (pageindex < 0):
        pageindex = 0

    if (not pagesize) or (pagesize < 0):
        pagesize = 10

    result = dbconn.find_keyword(keyword,pageindex,pagesize)
    if result:
        return render_template('list.html',articles = result,pageindex = pageindex,pagesize = pagesize,keyword = keyword)
    else:
        return redirect('/')


if __name__ == "__main__":

    app.run(port=8081)