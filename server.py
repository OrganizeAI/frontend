# create basic flask code
from io import BytesIO, StringIO
from flask import Flask, render_template, request, redirect, url_for, send_file
from image import maint
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


app = Flask(__name__)


@app.route("/")
def index():
    return "Main page"


@app.route("/urlupload", methods=["GET", "POST"])
def urlupload():
    if request.method == "POST":
        url = request.form["url"]
        c = maint(url)
        # c.show()
        return serve_pil_image(c)


app.run(debug=True)
