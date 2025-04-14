import sys
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Set up CORS and Talisman after the Flask app is created
CORS(app)
talisman = Talisman(app)  # Initialize Talisman here

# Import the routes after the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import, wrong-import-order
from service import routes, models  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # Initialize the database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)  # Exit if the database cannot be initialized

app.logger.info("Service initialized!")


