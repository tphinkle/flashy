# Imports

# Flashcard
import db_functions
import db_server
import flashcard_functions
import functions



def create_new_flashcard(user_id, front, back, labels, current_datetime):
    labels = functions.convert_scalar_to_list(labels)
    flashcard_id = db_functions.insert_flashcard(front, back)
    db_functions.insert_user_flashcard_relation(user_id, flashcard_id, labels, flashcard_functions.base_decay_rate, current_datetime)



def register_user_flashcard_action(user_id, flashcard_id, action, current_datetime):
    # Insert new row into user_flashcard_activity
    db_functions.insert_user_flashcard_activity(user_id, flashcard_id, action, current_datetime)

    # Get new decay time and update user_flashcard_relation
    user_flashcard_relation = db_functions.get_user_flashcard_relations_by_user_id_flashcard_id(user_id, flashcard_id)
    last_action_time = user_flashcard_relation['last_action_time']
    last_decay_time = user_flashcard_relations['decay_rate']
    new_decay_time = flashcard_functions.get_new_decay_time(last_decay_time, current_datetime, action)
    db_functions.update_user_flashcard_relation(user_id, flashcard_id, action)



def get_next_flashcard_by_user_id(user_id, current_datetime):

        # Get users' flashcard relations
        user_flashcard_relations = db_functions.get_user_flashcard_relations_by_user_id(user_id)


        # User has no flashcards
        if len(user_flashcard_relations) == 0:
            return None

        else:
            flashcard_id = flashcard_functions.get_next_flashcard_id(user_flashcard_relations, current_datetime)
            flashcard = db_functions.get_flashcards_by_flashcard_ids(flashcard_id)[0]

            return flashcard
