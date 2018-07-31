# Imports

# Python standard library
import json
import sys
import os

# Postgres and SQL
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# Flask
import werkzeug.security


# Scientific computing
import numpy as np

# Program specific
sys.path.append('..')
import main
import flashcard
import sql_server




def register_user(email_address, password, name):
    user = sql_server.SQLServer.get_user_by_email(email_address)


    # Invalid e-mail address
    if '@' not in email_address:
        return False

    # User doesn't already exist
    if user == None:
        print('adding new user!')
        print(password)
        hashed_password = hash_password(password)
        sql_server.SQLServer.add_user(email_address, hashed_password, name)
        return True

    # User already exists
    else:
        return False


def login_user(email_address, password):
    user = sql_server.SQLServer.get_user_by_email(email_address)

    expected_hashed_password = user['password']
    # User does not exist
    if user == None:
        return False



    # Correct password
    if werkzeug.security.check_password_hash(expected_hashed_password, password):
        print('successful login')
        return True
    # Incorrect password
    else:
        print('unsuccessful login')
        return False


def hash_password(password):
    hashed_password = werkzeug.security.generate_password_hash(password)
    return hashed_password
