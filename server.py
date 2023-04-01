from flask import *
from database import *
from forecast import *
from panel import create_schedule

class Reply:
    error = lambda: (jsonify({'error': 'L+ratio+you fell off'}), 500)
    ok = lambda: Response(status=200)
    # def __getattr__(self, name):
        # return getattr(Reply, name)()
# Reply = Reply()

app = Flask(__name__)

app.route('/')(lambda: redirect(url_for('static', filename='index.html')))

@app.route('/getPanelData', methods=['POST'])
def getPanelData():
    data = request.get_json()
    panel = get_panel(data['id'])
    if panel:
        return jsonify(panel)
    return Reply.error()

@app.route('/addPanel', methods=['POST'])
def addPanel():
    data = request.get_json()
    set_panel(data)
    return Reply.ok()

@app.route('/setPanelData', methods=['POST'])
def setPanelData():
    data = request.get_json()
    merge_panel(data)
    return Reply.ok()

@app.route("/getForecast", methods=["POST"])
def getForecast():
	data = request.get_json()
	return jsonify(forecast(data["latitude"], data["longitude"], data["timezone"]))

@app.route("/getPanelSchedule", methods=["POST"])
def getPanelSchedule():
    data = request.get_json()
    panel = get_panel(data['id'])
    if not panel:
        return Reply.error()
    return jsonify(create_schedule(panel))