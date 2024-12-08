from datetime import datetime
from flask import Blueprint, current_app, send_file
import os
from PIL import Image, ImageFont, ImageDraw
from tempfile import TemporaryDirectory

routes = Blueprint('routes', __name__)

numfreshness = 0
tempfolder = TemporaryDirectory()

def generate_image(key):
    img = Image.new("RGB", (500, 500))
    draw = ImageDraw.Draw(img)
    draw.multiline_text((10, 10), f"Anuncio {key}", font=ImageFont.load_default(size=75))
    draw.multiline_text((10, 100), datetime.now().strftime("%H:%M:%S"), font=ImageFont.load_default(size=75))
    img.save(f"{tempfolder.name}/{key}.jpg")

# Returns OK if images are still fresh, KO otherwise
@routes.route('/freshness')
def get_freshness():
    global numfreshness
    global tempfolder
    if numfreshness > 1:
        current_app.logger.info("Generate new images")
        numfreshness = 0
        for i in range(1,current_app.config["NUM_KEYS"]+1):
            generate_image(i)
        return "KO"
    else:
        numfreshness += 1
        return "OK"

# Returns the requested image
@routes.route('/image/<key>')
def get_image(key):
    # Image generation last resource
    if not os.path.exists(f"{tempfolder.name}/{key}.jpg"):
        generate_image(key)
    return send_file(f"{tempfolder.name}/{key}.jpg", mimetype='image/jpeg')
