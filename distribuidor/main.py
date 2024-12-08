from flask import Flask
import logging
from routes import routes

# Init app
app = Flask(__name__)

# Register routes
app.register_blueprint(routes)

# Set default configuration, then read environment vars
app.config.update(
    LOG_LEVEL = "INFO",
    CACHE_TIME = 5,
    GENERATOR_HOST = "127.0.0.1:5001"
)
app.config.from_prefixed_env("DISTRIBUITOR")

# Set error level
app.logger.setLevel(app.config["LOG_LEVEL"])

if __name__ == '__main__':
    # Main directly called
    app.run(host="0.0.0.0", port=5001)
else:
    # Main not directly called (probably using gunicorn)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
