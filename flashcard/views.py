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
import flashcard_server
import users


# Enables javascript requests json
CORS(main.app)


# Define views
views = flask.Blueprint('views', __name__)



def format_file_path_for_routing(file_path):
    file_path = file_path.replace(main.FLASHCARD_BASE_DIRECTORY, '')
    return file_path


def get_request_json(request):
    return request.form.to_dict(flat=False)




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
        if 'username' in flask.session:
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')

    elif method == 'POST':



        request_json = get_request_json(flask.request)


        # Log in user
        if 'login' in request_json.keys():
            print('login')
            login_email_address = request_json['login_email_address'][0]
            login_password = request_json['login_password'][0]

            login_success = users.login_user(login_email_address, login_password)



        # Register user
        elif 'register' in request_json.keys():
            print('register')
            register_email_address = request_json['register_email_address'][0]
            register_password = request_json['register_password'][0]
            register_name = request_json['register_name'][0]

            login_success = users.register_user(register_email_address, register_password, register_name)

            if login_success:
                login_email_address = register_email_address


        if login_success:
            flask.session['username'] = login_email_address
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')





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


        request_json = get_request_json(flask.request)



        flashcard_server.FlashCardServerPostGres.save_flashcard(request_json)






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
    new_flashcard = flashcard_server.FlashCardServerPostGres.get_next_flashcard()


    new_flashcard_json = flask.jsonify(new_flashcard)


    return new_flashcard_json


@views.route('/login')
def login():
    return flask.render_template('login.html')
