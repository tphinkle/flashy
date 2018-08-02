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
import user


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
            print(flask.session)
            print('user (index!)', flask.session['user_id'])
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')

    elif method == 'POST':



        request_json = get_request_json(flask.request)


        # Log in user
        if 'login' in request_json.keys():
            email = request_json['login_email_address'][0]
            password = request_json['login_password'][0]

            user_id = user.login_user(email, password)



        # Register user
        elif 'register' in request_json.keys():
            email = request_json['register_email_address'][0]
            password = request_json['register_password'][0]
            name = request_json['register_name'][0]

            user_id = user.register_user(email, password, name)




        if user_id != None:
            flask.session['username'] = email
            flask.session['user_id'] = user_id

            print('user id!!!', flask.session['user_id'])

            return flask.render_template('index.html')

        else:
            return flask.render_template('login.html')


@views.route('/login')
def login():
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
        user_id = flask.session['user_id']

        request_json = get_request_json(flask.request)
        front = request_json['new_flashcard_front'][0]
        back = request_json['new_flashcard_back'][0]
        labels = request_json['new_flashcard_label'][0]
        flashcard.FlashCardServer.create_new_flashcard(user_id, front, back, labels)



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



@views.route('/flashcard', methods = ['GET'])
def flashcard_get():


    next_flashcard = flashcard.FlashCardServer.get_next_flashcard(flask.session['user_id'])
    print(next_flashcard)
    next_flashcard_json = flask.jsonify(next_flashcard)

    print('jsoooon', next_flashcard_json)


    return next_flashcard_json


@views.route('/flashcard/submit/answer=<answer>', methods = ['POST'])
def flashcard_post(answer):


    data = flask.request.get_json()
    flashcard_id = data['flashcard_id']
    user_id =flask.session['user_id']



    return '201'
