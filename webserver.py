# basic html page servering:

from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
