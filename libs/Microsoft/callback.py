import json
import minecraft_launcher_lib as mine
import launcherlib
import flask
from flask import request

app = flask.Flask(__name__)
@app.route('/',methods = ['GET'])
def callback():
    data=request.args.to_dict()
    if data:
        print(data["code"])
    account_information = mine.microsoft_account.get_authorization_token("76658556-e195-49da-a47e-3c1eb90f6f9b", "ZXb8Q~pG0a15g4LqACHuHfLj3gfDpMY.4YJscc8ed", "http://localhost:13372",data["code"], launcherlib.verifier)
    print(account_information)
    return flask.render_template("index.html")

app.run(host="0.0.0.0",port=13372)