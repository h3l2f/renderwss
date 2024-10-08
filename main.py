from flask import *
import requests
from flask_cors import CORS
from flask_sock import Sock
import json
import io

app = Flask(__name__)
sock = Sock(app)
CORS(app)

@app.route("/")
def hp():
    return "NOTHING!"

@app.route("/pass/<code>")
def funct(code):
    ip = request.args.get("ip")
    filename = request.args.get("file")
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    stt = resp.text
    
    if (filename != "") and (filename != None) and ("ok" in stt):
        requests.get(f"https://flaskvs.vercel.app/m/IP {ip} for: {filename}.{code}")

    return stt

@app.route("/ping/<code>")
def _ping(code):
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    return resp.text

@app.route("/banip/<ip>")
def _bip(ip):
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
    return resp.text

@app.route("/del/<code>")
def _del(code):
    resp = requests.get(f"https://scamff.pythonanywhere.com{request.full_path}")
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
    nl = name.split(".")
    imgl = ["png","jpg","jpeg","gif"]

    if nl[len(nl)-1] not in imgl: return resp.text
    
    flo = io.BytesIO(resp.content)
    return send_file(flo, mimetype=f"image/{nl[len(nl)-1]}")

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
