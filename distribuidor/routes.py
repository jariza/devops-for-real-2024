from flask import Blueprint, current_app, render_template, send_file
import glob
import os
from platform import node
import requests
from tempfile import TemporaryDirectory

routes = Blueprint('routes', __name__)

# Create temporary folder
tempfolder = TemporaryDirectory()

invalidate = False
cachecurrlive = 0

# Returns the advertisement
@routes.route('/')
def get_root():
    global cachecurrlive
    global invalidate
    if cachecurrlive > current_app.config["CACHE_TIME"]:
        cachecurrlive = 0
        r = requests.get(f"http://{current_app.config['GENERATOR_HOST']}/freshness", stream=True)
        if r.status_code == 200:
            if r.text == "KO":
                current_app.logger.info("Invalidation")
                invalidate = True
    else:
        cachecurrlive += 1
    return render_template('index.html', hostname=node())

# Returns the requested image
@routes.route('/image<key>.jpg')
def get_image(key):
    global invalidate
    global tempfolder
    if invalidate:
        # Check that generator is available
        r = requests.get(f"http://{current_app.config['GENERATOR_HOST']}/image/{key}")
        if r.status_code == 200:
            for f in glob.glob(f"{tempfolder.name}/*.jpg"):
                os.remove(f)
            invalidate = False
    if not os.path.exists(f"{tempfolder.name}/{key}.jpg"):
        r = requests.get(f"http://{current_app.config['GENERATOR_HOST']}/image/{key}", stream=True)
        if r.status_code == 200:
            with open(f"{tempfolder.name}/{key}.jpg", 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    return send_file(f"{tempfolder.name}/{key}.jpg", mimetype='image/jpg')
