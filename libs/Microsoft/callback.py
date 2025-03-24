import json

import flask
from flask import request

app = flask.Flask(__name__)
@app.route('/',methods = ['GET'])
def callback():
    data=request.args.to_dict()
    if data:
        print(data["code"])
    return flask.render_template("index.html")

app.run(host="0.0.0.0",port=13372)