import json
import minecraft_launcher_lib as mine
import flask
from flask import request

from libs.Microsoft import launcherlib

_GLOBAL_FALLBACK_PORT = 13372

app = flask.Flask(__name__)
@app.route('/',methods = ['GET'])
def callback():
    data=request.args.to_dict()
    if data:
        print(data["code"])
    account_information = mine.microsoft_account.get_authorization_token("ece1bc0c-e3d1-4967-b4a2-63d13c57380c", "A1R8Q~IM5hO.SqAAdNhgoTVESemehVsCMS3ukde~", f"http://localhost:{_GLOBAL_FALLBACK_PORT}",data["code"], launcherlib.verifier)
    print(account_information)
    return flask.render_template("index.html")

app.run(host="0.0.0.0",port=_GLOBAL_FALLBACK_PORT)