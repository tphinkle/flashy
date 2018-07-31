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
import flashcard
import sql_server




class FlashCardServer(object):

    form_translator_dict = {
        'form_front': 'front',
        'form_back': 'back',
        'form_label': 'label'
    }



    def save_flashcard(flashcard):

        # Convert field names
        temp_flashcard = {}
        for key, value in flashcard.items():
            temp_flashcard[FlashCardServer.form_translator_dict[key]] = value
        flashcard = temp_flashcard

        # Convert values to scalar if list
        for key in ['front', 'back']:
            if type(flashcard[key]) == list:
                flashcard[key] = flashcard[key][0]

        front = flashcard['front']
        back = flashcard['back']
        labels = flashcard['label']

        sql_server.SQLServer.insert_flashcard(front, back, labels)



        return


    def get_next_flashcard():


        flashcards = SQLServer.load_all_flashcards()

        i = np.random.randint(0, len(flashcards))

        print(i, flashcards[i])

        return flashcards[i]






class FlashCard(object):
    def __init__(flashcard_json):
        self._id = flashcard_json['id']
        self._text = flashcard_json['card']['text']
        self._labels = flashcard_json['labels']
