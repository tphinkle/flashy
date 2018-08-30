# Imports

# Python standard library
import json
import datetime
import sys
import os

# Postgres and SQL
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# Scientific computing
import numpy as np

# Flashcard
sys.path.append('..')
import db_functions
import functions
import main






USER_FLASHCARD_ACTIVITY_TYPES = ["correct", "incorrect"]
base_decay_time = 7*24*60*60


def update_decay_time(old_decay_time, current_datetime, action_type):

    dt = (current_datetime - last_action_time).seconds
    if activity_type == 'correct':
        new_decay_time = dt + decay_time
    elif activity_type == 'incorrect':
        new_decay_time = dt - decay_time
        min_decay_time = 60*60*24
        if new_decay_time < min_decay_time:
            new_decay_time = min_decay_time

    return new_decay_time


def get_p_recall(dt, decay_time):
    return np.exp(-dt/decay_time)

def get_next_flashcard_id(user_flashcard_relations, current_datetime):

    # Calculate recall probability
    dts = [(current_datetime - user_flashcard_relation['last_action_time']).seconds for user_flashcard_relation in user_flashcard_relations]
    decay_times = [user_flashcard_relation['decay_time'] for user_flashcard_relation in user_flashcard_relations]
    p_recalls = [get_p_recall(dt, decay_time) for dt, decay_time in zip(dts, decay_times)]

    # Select flashcard with lowest recall probability and return
    user_flashcard_relation = user_flashcard_relations[np.argmin(p_recalls)]
    flashcard_id = user_flashcard_relation['flashcard_id']

    return flashcard_id
