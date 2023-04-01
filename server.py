from flask import *
from database import *
from forecast import *
from panel import create_schedule
from time import time

class Reply:
    def error(): return (jsonify({'error': 'L+ratio+you fell off'}), 500)
    def ok(): return Response(status=200)


global_forecast, last_forcast_update_time = None, 0
def get_forecast():
    global global_forecast
    if time() > last_forcast_update_time + 60:
        global_forecast = internal_forecast(
            (36.0663068, -94.1738257, "America/Chicago"))
    return global_forecast


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
    return jsonify(create_schedule(internal_forecast(data["latitude"], data["longitude"], data["timezone"]), panel))
