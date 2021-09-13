"""The Python MagicPod Excute."""

import browser_action

from flask import Flask
from flask import request

import os

app = Flask(__name__)
chrome = browser_action.Chrome()

@app.route("/")
def index():
    return "Hello API!"


@app.route("/sample", methods=["GET"])
def run_everyday():
    chrome.open_run_task(sample_function,False)

    return "SUCCESSED!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.getenv("PORT", 8080)))
