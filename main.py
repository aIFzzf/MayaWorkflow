from flask import json
from flask import request
from flask import Flask


app = Flask(__name__)

@app.route('/Maya')
def api_message():
    # return "Test"
    if request.headers['Content-Type'] == 'application/json':
        my_info = json.dumps(request.json)
        print "test"
        return my_info


if __name__ == '__main__':
    app.run(debug=True)