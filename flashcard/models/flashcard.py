# Imports

# Python standard library
import json
import sys
import os

# Postgres and SQL
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# Scientific computing
import numpy as np

# Program specific
sys.path.append('..')
import main
import sql_server


def convert_to_list(scalar):
    if type(scalar) != list:
        return [scalar]


class FlashCardServer(object):


    def create_new_flashcard(user_id, front, back, labels):
        labels = convert_to_list(labels)

        flashcard_id = sql_server.SQLServer.add_flashcard_to_flashcards(front, back, labels)
        sql_server.SQLServer.add_user_flashcard_to_user_flashcard_relations(user_id, flashcard_id)

        return flashcard_id




    def get_next_flashcard(user_id):


        flashcards = sql_server.SQLServer.get_flashcards_by_user_id(user_id)

        i = np.random.randint(0, len(flashcards))

        flashcard = flashcards[i]



        return flashcard
