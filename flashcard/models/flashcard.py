# Imports

# Python standard library
import json
import sys
import os

# Scientific computing
import numpy as np

# Program specific
sys.path.append('..')
import main














class FlashCardServer(object):


    form_translator_dict = {
        'form_front': 'front',
        'form_back': 'back',
        'form_label': 'label'
    }


    flashcard_file_directory = main.FLASHCARD_DATA_DIRECTORY + '/cards/'


    def get_new_flashcard_id():

        # Get all files
        flashcard_file_names = FlashCardServer.get_flashcard_file_names()


        # Get IDs
        flashcard_ids = [int(flashcard_file_name.split('.')[0]) for flashcard_file_name in flashcard_file_names]

        # Handle empty case
        if len(flashcard_ids) == 0:
            return '000000000'

        # Increment by one
        max_flashcard_id = max(flashcard_ids)
        new_flashcard_id = max_flashcard_id + 1

        # Format with billion precision
        new_flashcard_id = str(new_flashcard_id).zfill(9)
        return new_flashcard_id


    def get_flashcard_file_paths():
        flashcard_file_names = FlashCardServer.get_flashcard_file_names()
        flashcard_file_paths = [FlashCardServer.flashcard_file_directory + flashcard_file_name for flashcard_file_name in flashcard_file_names]
        return flashcard_file_paths


    def get_flashcard_file_names():
        # Get all files in folder
        flashcard_file_names = [flashcard_file_name for flashcard_file_name in os.listdir(FlashCardServer.flashcard_file_directory)]

        # Filter out non-flashcard type files (e.g., .DSSTORE)
        flashcard_file_names = [flashcard_file_name for flashcard_file_name in flashcard_file_names if flashcard_file_name[0] != '.']


        return flashcard_file_names


    def get_flashcard_file_name_from_flashcard_id(flashcard_id):
        return flashcard_id + '.json'



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

        # Get new ID and attach
        flashcard_id = FlashCardServer.get_new_flashcard_id()
        flashcard['id'] = flashcard_id

        # Save to file
        save_directory = FlashCardServer.flashcard_file_directory
        save_name = FlashCardServer.get_flashcard_file_name_from_flashcard_id(flashcard_id)
        save_path = save_directory + save_name
        with open(save_path, 'w') as save_file_handle:
            json.dump(flashcard, save_file_handle)

        return






    def load_all_flashcards(order = None):

        # Open all flashcards
        flashcard_file_paths = FlashCardServer.get_flashcard_file_paths()

        flashcards = []
        for flashcard_file_path in flashcard_file_paths:
            with open(flashcard_file_path, 'r') as flashcard_file_handle:

                flashcard_str = flashcard_file_handle.read()
                flashcard_dict = json.loads(flashcard_str)
                flashcards.append(flashcard_dict)


        return flashcards

    def get_next_flashcard():
        flashcards = FlashCardServer.load_all_flashcards()

        i =  np.random.randint(0,len(flashcards))

        return flashcards[i]






class FlashCard(object):
    def __init__(flashcard_json):
        self._id = flashcard_json['id']
        self._text = flashcard_json['card']['text']
        self._labels = flashcard_json['labels']
