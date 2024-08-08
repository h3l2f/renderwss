from flask import *
import requests
from flask_cors import CORS
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)
CORS(app)

@app.route("/")
def hp():
    return "NOTHING!"

@app.route("/pass/<code>")
def funct(code):
    filename = request.args.get("file")
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    stt = resp.text
    
    if (filename != "") and (filename != None) and (stt == "ok"):
        requests.get(f"https://flaskvs.vercel.app/m/{filename}.{code}")

    return stt

@app.route("/ping/<code>")
def _ping(code):
    resp = requests.get(f"https://scamff.pythonanywhere.com/ping/{code}")
    return resp.text

@app.route("/add-pass/<code>")
def add_pass(code):
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    return resp.text

@app.route("/hh")
def hh():
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    return resp.text

@app.route('/file/<name>')
def gfile(name):
    resp = requests.get(f"https://scamff.pythonanywhere.com/file/{name}")
    return resp.text

@sock.route("/verify")
def verify(ws):
    payload = {
        "status":"",
        "code":""
    }
    code = (ws.receive()).replace(" ","")
    if code.count("|") > 1: ws.send("Format: password (|Optional: file_name)")
    else:
        code = code.split("|")
        passwd = code[0]
        filename = code[1] if len(code) == 2 else ""
        resp = requests.get(f"https://scamff.pythonanywhere.com/pass/{passwd}")
        if resp.text == "ok":
            if len(code) == 1:
                payload["status"] = "ok"
                return ws.send(str(payload))
            resp = requests.get(f"https://scamff.pythonanywhere.com/file/{filename}")
            if '{"error"' not in resp.text:
                payload["status"] = "ok"
                payload["code"] = resp.text
                ws.send(str(payload))
            else:
                payload["status"] = "nf"
                ws.send(str(payload))
        else:
            payload["status"] = "err"
            ws.send(str(payload))
    

if __name__ == "__main__":
    app.run()
