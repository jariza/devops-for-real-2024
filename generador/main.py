from flask import Flask
from routes import generate_image, routes
import logging

# Init app
app = Flask(__name__)

# Register routes
app.register_blueprint(routes)

# Set default configuration, then read environment vars
app.config.update(
    LOG_LEVEL = "INFO",
    NUM_KEYS = 4
)
app.config.from_prefixed_env("CREATOR")

# Set error level
app.logger.setLevel(app.config["LOG_LEVEL"])

# First generation of images
for i in range(1,app.config["NUM_KEYS"]+1):
    generate_image(i)

if __name__ == '__main__':
    # Main directly called
    app.run(host="0.0.0.0", port=5000)
else:
    # Main not directly called (probably using gunicorn)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
