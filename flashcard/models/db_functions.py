# Imports

# Flashcard related
import functions
import db_server



'''
Flashcard
'''

def get_flashcards_by_flashcard_ids(flashcard_ids, fields = '*'):
    table_name = 'flashcards'
    flashcard_ids = functions.convert_scalar_to_list(flashcard_ids)
    predicates = [{
        'field': 'flashcard_id',
        'operator': 'in',
        'values': flashcard_ids
    }]

    flashcards = db_server.DBServer.select(table_name, fields, predicates)

    return flashcards



'''
User Flashcard Activity
'''
def insert_user_flashcard_activity(user_id, flashcard_id, activity_type, current_datetime):
    table_name = 'user_flashcard_activity'
    data = {
        'user_id': user_id,
        'flashcard_id': flashcard_id,
        'flashcard_action_name': activity_type,
        'datetime': current_datetime
    }
    db_server.DBServer.insert(table_name, data)


'''
User Flashcard Relations
'''

def get_user_flashcard_relations_by_user_id_flashcard_id(user_id, flashcard_id, fields = '*'):
    table_name = 'user_flashcard_relations'
    predicates = [{
        'field': 'user_id',
        'operator': '=',
        'values': user_id},
        {'field': 'flashcard_id',
        'operator': '=',
        'values': flashcard_id
    }]


    user_flashcard_relation = db_server.DBServer.select(table_name, fields, predicates)


    return user_flashcard_relation



def get_user_flashcard_relations_by_user_id(user_id):
    # Get all user's flashcards
    table_name = 'user_flashcard_relations'
    fields = '*'
    predicates = [{
        'field': 'user_id',
        'operator': '=',
        'values': user_id
    }]
    user_flashcard_relations = db_server.DBServer.select(table_name, fields, predicates)

    return user_flashcard_relations
