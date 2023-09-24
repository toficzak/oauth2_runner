from flask import Flask, request
import requests
import webbrowser

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['GET'])
def init_login():
    webbrowser.open('http://localhost:8080/realms/test/protocol/openid-connect/auth?response_type=code&scope=email&client_id=test&redirect_uri=http://localhost:5000/callback', new=2)
    return "ok"

@app.route("/callback", methods=['GET'])
def input_access_token():
    args = request.args
    print(args)
    code = args.to_dict()["code"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    params = {
        "grant_type": "authorization_code",
        "client_id": "test",
        "client_secret":"6kQHYQGUWTj7W41awLXFxNqgUkGpFo4h",
        "redirect_uri": "http://localhost:5000/callback"
    }

    params["code"] = code

    resp = requests.post("http://localhost:8080/realms/test/protocol/openid-connect/token", data=params, headers=headers)
    access_token = resp.json()["access_token"]
    print(access_token)
    return access_token