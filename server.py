# from flask import Flask, render_template, send_from_directory, redirect, url_for
from sqlitedict import SqliteDict
from flask import *
database = SqliteDict("database.sqlite", tablename="product", autocommit=True)

app = Flask(__name__)

app.route('/')(lambda: redirect(url_for('static', filename='index.html')))

@app.route('/api')
def api():
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    return jsonify(data)