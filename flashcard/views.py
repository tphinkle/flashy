# Imports

# Python standard library
import datetime
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
import server
import user



# Enables javascript requests json
CORS(main.app)


# Define views
views = flask.Blueprint('views', __name__)


# For URL Query parameter, use request.args
# For Form input, use request.form
# For data type application/json, use request.data -> request.get_json()






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


        form_data = flask.request.form.to_dict(flat = False)

        print(form_data)


        # Log in user
        if 'login' in form_data.keys():
            email = form_data['login_email_address'][0]
            password = form_data['login_password'][0]

            user_id = user.login_user(email, password)



        # Register user
        elif 'register' in form_data.keys():
            email = form_data['register_email_address'][0]
            password = form_data['register_password'][0]
            name = form_data['register_name'][0]

            user_id = user.register_user(email, password, name)




        if user_id != None:
            flask.session['username'] = email
            flask.session['user_id'] = user_id

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
        user_id = get_user_id_by_session(flask.session)
        form_data = flask.request.form.to_dict(flat = False)


        front = form_data['new_flashcard_front'][0]
        back = form_data['new_flashcard_back'][0]
        labels = form_data['new_flashcard_label'][0]
        current_datetime = datetime.datetime.now()
        server.create_new_flashcard(user_id, front, back, labels, current_datetime)



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


    # Get next flashcard and user info
    current_datetime = datetime.datetime.now()
    next_flashcard = server.get_next_flashcard_by_user_id(flask.session['user_id'], current_datetime)


    if next_flashcard:
        return_json = flask.jsonify(next_flashcard)
        return return_json
    else:
        return '404'


@views.route('/flashcard/submit', methods = ['POST'])
def flashcard_post():

    user_id = get_user_id_by_session(flask.session)

    data = flask.request.get_json()
    flashcard_id = data['flashcard_id']
    answer = data['answer']
    date = datetime.datetime.now()

    server.register_user_flashcard_action(user_id, flashcard_id, answer, date)

    return '201'


def get_user_id_by_session(session):
    user_id = str(session['user_id'])
    return user_id




def format_request(request):

    for key, value in request.items():
        request[key] = str(value)

    return request
