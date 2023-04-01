from flask import *
from database import *

class Response:
    error = jsonify({'error': 'L+ratio+you fell off'}), 500
    ok = Response(status=200)

app = Flask(__name__)

app.route('/')(lambda: redirect(url_for('static', filename='index.html')))

@app.route('/getPanelData', methods=['POST'])
def getPanelData():
    data = request.get_json()
    panel = get_panel(data['id'])
    if panel:
        return jsonify(panel)
    return Response.error

@app.route('/addPanel', methods=['POST'])
def getPanelData():
    data = request.get_json()
    set_panel(data)
    return Response.ok

@app.route('/setPanelData', methods=['POST'])
def getPanelData():
    data = request.get_json()
    merge_panel(data)
    return Response.ok