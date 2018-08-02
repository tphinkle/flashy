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
import sql_server



USER_FLASHCARD_ACTIVITY_TYPES = ["CORRECT", "INCORRECT"]

def register_user_flashcard_activity(user_id, flashcard_id, activity_type):

    if activity_type not in USER_FLASHCARD_ACTIVITY_TYPES:
        return

    sql_server.add_user_flashcard_action_to_user_flashcard_activity(user_id, flashcard_id, activity_type)
