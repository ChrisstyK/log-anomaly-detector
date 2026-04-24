from flask import Flask, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

def log_event(ip, action, status):
    file_exists = os.path.isfile("logs.csv")

    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "ip", "action", "status"])

        writer.writerow([datetime.now(), ip, action, status])


@app.route("/")
def home():
    ip = request.remote_addr
    log_event(ip, "visit", "success")
    return "Home"


@app.route("/login")
def login():
    ip = request.remote_addr
    password = request.args.get("password")

    if password == "admin":
        log_event(ip, "login", "success")
        return "Login OK"
    else:
        log_event(ip, "login", "failed")
        return "Login FAILED"


@app.route("/download")
def download():
    ip = request.remote_addr
    log_event(ip, "download", "success")
    return "Download"


if __name__ == "__main__":
    app.run(debug=True)