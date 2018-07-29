# Imports
import flask
import os
from werkzeug.utils import secure_filename    # Needed for image upload
import sys

# Base path for project
FLASHCARD_BASE_DIRECTORY = os.path.dirname(__file__)
FLASHCARD_DATA_DIRECTORY = FLASHCARD_BASE_DIRECTORY + '/data/'


# Configure app
app = flask.Flask(__name__)
app.config.from_object(__name__) # Load config from thsie file (permit_generator.py)
app.config.update(dict(
SECRET_KEY = 'key',
USERNAME = 'admin',
PASSWORD = 'default'
))




# Register view blueprints
sys.path.append(FLASHCARD_BASE_DIRECTORY)
import views
app.register_blueprint(views.views)



if __name__ == '__main__':
    app.run()
