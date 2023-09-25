from flask import Flask, request
import requests
import webbrowser
import os

app = Flask(__name__)


@app.route("/login", methods=['GET'])
def init_login():
    idp_url = os.environ['ms_idp_url']
    client_id = os.environ['ms_client_id']
    callback_url = os.environ['ms_redirect_uri']
    url = idp_url + ('/realms/test/protocol/openid-connect/auth'
                     '?response_type=code'
                     '&scope=email' +
                     '&client_id=' + client_id +
                     '&redirect_uri=' + callback_url)
    webbrowser.open(url, new=2)
    return "ok"


@app.route("/callback", methods=['GET'])
def input_access_token():
    client_id = os.environ['ms_client_id']
    client_secret = os.environ['ms_client_secret']
    redirect_uri = os.environ['ms_redirect_uri']

    args = request.args
    print(args)
    code = args.to_dict()["code"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }

    params["code"] = code

    idp_url = os.environ['ms_idp_url']
    idp_realm = os.environ['ms_idp_realm']
    url = idp_url + "/realms/" + idp_realm + "/protocol/openid-connect/token"
    resp = requests.post(url, data=params, headers=headers)
    access_token = resp.json()["access_token"]
    print(access_token)
    return access_token
