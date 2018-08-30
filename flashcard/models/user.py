# Imports

# Python standard library
import json
import sys
import os


# Flask
import werkzeug.security

# Program specific
sys.path.append('..')
import main
import db_server


def register_user(email_address, password, name):
    user = db_server.DBServer.get_users_by_email(email_address)


    # Invalid e-mail address
    if '@' not in email_address:
        return None

    # User doesn't already exist
    if user == None:
        hashed_password = hash_password(password)
        user_id = db_server.DBServer.add_user_to_users(email_address, hashed_password, name)
        return user_id

    # User already exists
    else:
        return None


def login_user(email_address, password):
    user = db_server.DBServer.get_users_by_email(email_address)

    # User does not exist
    if user == None:
        return None

    # Correct password
    expected_hashed_password = user['password']
    if werkzeug.security.check_password_hash(expected_hashed_password, password):
        return user['user_id']

    # Incorrect password
    else:
        return None


def hash_password(password):
    hashed_password = werkzeug.security.generate_password_hash(password)
    return hashed_password
