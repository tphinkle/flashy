# Imports

# Python standard library
import json
import os
import sys


# Flask
import flask
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin




# Program specific
import main
sys.path.append(main.FLASHCARD_BASE_DIRECTORY + '/models')
import flashcard


# Enables javascript requests json
CORS(main.app)


# Define views
views = flask.Blueprint('views', __name__)



def format_file_path_for_routing(file_path):
    file_path = file_path.replace(main.FLASHCARD_BASE_DIRECTORY, '')
    return file_path



@views.route('/', methods=['GET', 'POST'])
def index():
    '''
    The index; a simple interface for allowing a user to submit an image
    to query
    methods:
        GET: The main page, has a 'submit image' button
        POST: After the submit/query/request button is hit, the file will be saved
        to the server and the user will be redirected to the uploads page
    '''




    # Get method type
    method = flask.request.method


    # Get
    if method == 'GET':
        return flask.render_template('index.html')


@views.route('/add', methods = ['GET', 'POST'])
def add():
    '''
    Add flashcard page.
    '''

    # Get method type
    method = flask.request.method

    # Get
    if method == 'GET':
        return flask.render_template('add.html')

    elif method == 'POST':

        # Get data

        print(flask.request.form)


        request_json = flask.request.form.to_dict(flat=False)



        flashcard.FlashCardServer.save_flashcard(request_json)






        return flask.render_template('add.html')



@views.route('/review', methods = ['GET'])
def review():
    '''
    Review flashcards page.
    '''

    # Get method type
    method = flask.request.method

    # Get
    if method == 'GET':
        return flask.render_template('review.html')



@views.route('/request_flashcard')
def request_flashcard():
    new_flashcard = flashcard.FlashCardServer.get_next_flashcard()

    print(new_flashcard['label'])

    new_flashcard_json = flask.jsonify(new_flashcard)

    return new_flashcard_json
