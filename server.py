from flask import *
from database import *

class Reply:
    error = lambda: (jsonify({'error': 'L+ratio+you fell off'}), 500)
    ok = lambda: Response(status=200)
    def __getattr__(self, name):
        return getattr(Reply, name)()
Reply = Reply()

def add_panel(panel: Panel):
    
    print('a' in database)

exit()
app = Flask(__name__)

app.route('/')(lambda: redirect(url_for('static', filename='index.html')))

@app.route('/getPanelData', methods=['POST'])
def getPanelData():
    data = request.get_json()
    panel = get_panel(data['id'])
    if panel:
        return jsonify(panel)
    return Reply.error

@app.route('/addPanel', methods=['POST'])
def addPanel():
    data = request.get_json()
    if get_panel(data['id']):
        return Reply.error
    set_panel(data)
    return Reply.ok

@app.route('/setPanelData', methods=['POST'])
def setPanelData():
    data = request.get_json()
    merge_panel(data)
    return Reply.ok
