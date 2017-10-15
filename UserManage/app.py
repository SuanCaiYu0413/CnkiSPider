# coding:utf-8

from MongoDB import DBConn
from flask import Flask,render_template,jsonify,request

app = Flask(__name__)
dbconn = DBConn()
dbconn.conn()


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search_cache')
def search_cache():
    keyword = request.args.get('keyword')
    return jsonify(dbconn.find_cache(keyword))


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    table = request.args.get('table')
    return jsonify(dbconn.find_keyword({'keyword':keyword,'table':table}))


if __name__ == "__main__":

    app.run(port=8080)