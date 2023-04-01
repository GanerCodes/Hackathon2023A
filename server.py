# from flask import Flask, render_template, send_from_directory, redirect, url_for
from sqlitedict import SqliteDict
from flask import *
from Panel import Panel
database = SqliteDict("panels.sqlite", tablename="panels", autocommit=True)

def add_panel(panel: Panel):
    
    print('a' in database)

exit()
app = Flask(__name__)

app.route('/')(lambda: redirect(url_for('static', filename='index.html')))

@app.route('/api')
def api():
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    return jsonify(data)