# imports
import io
import cv2
import urllib.request
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from requests_toolbelt import MultipartEncoder


def image_to_pil(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    print(img.shape)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    # Convert to JPEG Buffer
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="PNG")
    return pilImage, buffered


def fetch_robo(buffered):
    # Build multipart form and post request
    m = MultipartEncoder(
        fields={"file": ("imageToUpload", buffered.getvalue(), "image/png")}
    )

    response = requests.post(
        "https://detect.roboflow.com/organizeai/3?api_key=w0711nTh97u0WD2FC57t",
        data=m,
        headers={"Content-Type": m.content_type},
    )
    if response.status_code >= 400:
        print("Error:", response.text)
        return None
    return response.json()["predictions"]


def gen_labled_image(predictions, pilImage):
    image = pilImage

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("rob.ttf")

    for box in predictions:
        color = "#4892EA"
        x1 = box["x"] - box["width"] / 2
        x2 = box["x"] + box["width"] / 2
        y1 = box["y"] - box["height"] / 2
        y2 = box["y"] + box["height"] / 2

        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)

        if True:
            text = box["class"]
            text_size = font.getsize(text) * 2

            # set button size + 10px margins
            button_size = (text_size[0] + 5, text_size[1] + 5)
            button_img = Image.new("RGBA", button_size, color)
            # put text on button with 10px margins
            button_draw = ImageDraw.Draw(button_img)
            button_draw.text((5, 3), text, font=font, fill=(255, 255, 255, 100))

            # put button on source image in position (0, 0)
            image.paste(button_img, (int(x1), int(y1)))
    return image


def maint(url):
    # fetch image from url
    pilImage, buffered = image_to_pil(url)
    # fetch predictions from roboflow
    predictions = fetch_robo(buffered)
    # generate labled image
    labled_image = gen_labled_image(predictions, pilImage)
    # show labled image

    return labled_image
