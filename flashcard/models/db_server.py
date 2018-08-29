# Imports

# Python standard library
import csv
import datetime
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
import functions

def initialize_table_data():
    # Postgres settings
    dbname = 'flashy'
    username = 'prestonh'
    password = 'password'

    engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
    #print(engine.url)

    ## create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)
    #print('database load:', database_exists(engine.url))

    # Create tables (if they do not exist)

    conn = psycopg2.connect(f"dbname={dbname} user={username} host='localhost' password={password}")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)




    table_names = ['users', 'flashcards', 'user_flashcard_relations', 'user_site_activity', 'user_flashcard_activity']

    # Create user
    name = 'Preston'
    email = 'tphinkle@gmail.com'
    password = 'pbkdf2:sha256:50000$YjMprR18$23810d76048588d01a5b1dda93e07a202c3aa79bf0d86e90e107b305074fe4e8'
    time = datetime.datetime.now()
    query = """INSERT INTO users(name, email, date_created, password) VALUES (%s, %s, %s, %s) RETURNING user_id""";
    cur.execute(query, (name, email, time, password))
    conn.commit()
    user_id = cur.fetchone()['user_id']


    with open('../../data/flashcards.txt', 'r') as file_handle:
        reader = csv.reader(file_handle, delimiter = '\t')
        for row in reader:
            print(row)

            query = """INSERT INTO flashcards(front, back) VALUES (%s, %s) RETURNING flashcard_id""";
            cur.execute(query, (row[0], row[1]))
            conn.commit()

            labels = [row[2]]
            flashcard_id = cur.fetchone()['flashcard_id']

            decay_rate = 604800
            query = """INSERT INTO user_flashcard_relations(user_id, flashcard_id, labels, decay_rate, last_action_time) VALUES (%s, %s, %s, %s, %s);"""
            cur.execute(query, (user_id, flashcard_id, labels, decay_rate, time))











class DBServer(object):

    # Postgres settings
    dbname = 'flashy'
    username = 'prestonh'
    password = 'password'

    engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
    #print(engine.url)

    ## create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)
    #print('database load:', database_exists(engine.url))

    # Create tables (if they do not exist)

    conn = psycopg2.connect(f"dbname={dbname} user={username} host='localhost' password={password}")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)




    table_names = ['users', 'flashcards', 'user_flashcard_relations', 'user_site_activity', 'user_flashcard_activity']
    for table_name in table_names:
        cur.execute(f"""SELECT COUNT(*) FROM {table_name} LIMIT 1;""")









    def _format_query(table_name, fields, predicates):

        query = '''SELECT'''
        args = []

        # Fields
        fields = functions.convert_scalar_to_list(fields)
        for i, field in enumerate(fields):
            if field == '*':
                query = ' '.join([query, '*'])
            else:
                query = ' '.join([query, '%s'])
                args.append(field)
            if i != len(fields) - 1:
                query = ' '.join([query, ','])


        # Table name
        query = ' '.join([query, 'FROM', table_name])

        # Predicates
        predicates = functions.convert_scalar_to_list(predicates)
        if len(predicates) > 0:
            query = ' '.join([query, 'WHERE'])

        for i, predicate in enumerate(predicates):
            query = ' '.join([query, predicate['field'], predicate['operator'], '%s'])
            if i != len(predicates) - 1:
                query = ' '.join([query, 'AND'])
            if predicate['operator'] == '=':
                args.append(predicate['values'])
            elif predicate['operator'] == 'in':
                args.append(tuple(predicate['values']))



        # Convert to tuple
        args = tuple(args)



        print('query, args', query, args)
        return query, args



    def select(table_name, fields, predicates):

        # Fields
        query, args = DBServer._format_query(table_name, fields, predicates)

        # Execute query and get info
        DBServer.cur.execute(query, args)
        data = DBServer.cur.fetchall()


        return data

    def insert(table_name, data, returning = None):
        command = '''INSERT INTO'''

        # table name
        command = ' '.join([command, table_name])

        # column names
        command = command + '(' + ' '.join([key for key in data.keys()]) + ')'

        # values
        command = command + 'VALUES (' + ' '.join(['%s' for i in range(len(data))]) + ')'

        if returning:
            command = ' '.join([command, 'RETURNING', returning])

        # Execute command
        print(command)
        DBServer.cur.execute(command, functions.convert_to_tuple(data.values()))



























































    '''
    USERS
    '''


    def get_users_by_email(email):


        email = functions.convert_to_tuple(email)


        # Insert into table
        query = f"""SELECT * FROM users WHERE email IN %s;"""
        DBServer.cur.execute(query, (email, ))
        user = DBServer.cur.fetchone()
        return user




    def add_user_to_users(email, password, name):


        # Date created
        date_created = datetime.datetime.now()

        # Insert into table
        query = """INSERT INTO users(email, password, name, date_created) VALUES (%s, %s, %s, %s) RETURNING user_id;"""
        DBServer.cur.execute(query, (email, password, name, date_created))
        DBServer.conn.commit()
        user_id = DBServer.cur.fetchone()['user_id']

        return user_id


    '''
    FLASHCARDS
    '''

    def add_flashcard_to_flashcards(front, back):


        # Insert into table
        query = """INSERT INTO flashcards(front, back) VALUES (%s, %s) RETURNING flashcard_id;"""
        DBServer.cur.execute(query, (front, back))

        DBServer.conn.commit()
        flashcard_id = DBServer.cur.fetchone()['flashcard_id']
        return flashcard_id



    def get_flashcards_by_user_ids(user_ids):

        user_ids = functions.convert_to_tuple(user_ids)

        print(user_ids)

        query = f"""SELECT * FROM flashcards LEFT JOIN user_flashcard_relations ON \
            (flashcards.flashcard_id = user_flashcard_relations.flashcard_id) WHERE \
            user_flashcard_relations.user_id IN %s;"""


        DBServer.cur.execute(query, (user_ids, ));
        flashcards = DBServer.cur.fetchall()


        return flashcards

    def get_flashcards_by_flashcard_ids(flashcard_ids):

        flashcard_ids, = functions.convert_to_tuple(flashcard_ids)

        query = f"""SELECT * FROM flashcards WHERE flashcard_id IN %s;"""

        DBServer.cur.execute(query, (flashcard_ids, ))
        flashcards = DBServer.cur.fetchall()

        return flashcards;


    '''
    USER FLASHCARD RELATIONS
    '''


    def add_user_flashcard_to_user_flashcard_relations(user_id, flashcard_id, labels, decay_rate, date_time):
        # Insert into table
        #user_id, flashcard_id, labels = DBServer.format_insert_args(user_id, flashcard_id, labels)

        query = """INSERT INTO user_flashcard_relations(user_id, flashcard_id, labels, decay_rate, last_action_time) VALUES (%s, %s, %s, %s, %s);"""
        DBServer.cur.execute(query, (user_id, flashcard_id, labels, decay_rate, date_time))
        DBServer.conn.commit()

    def get_user_flashcard_relations_by_user_id(user_id):
        user_id, = convert_to_tuple(user_id)

        query = """SELECT * FROM user_flashcard_relations WHERE user_id IN %s;"""

        DBServer.cur.execute(query, (user_id, ))
        relations = DBServer.cur.fetchall()

        return relations

    def update_user_flashcard_relations(user_id, flashcard_id, new_decay_rate, new_date_time):
        query = """UPDATE user_flashcard_relations SET new_decay_rate = %s WHERE user_id = %s AND flashcard_id = %s""";
        DBServer.cur.execute(query, (user_id, flashcard_id, new_decay_rate))
        query = """UPDATE user_flashcard_relations SET new_date_time = %s WHERE user_id = %s AND flashcard_id = %s""";
        DBServer.cur.execute(query, (user_id, flashcard_id, new_date_time))






    '''
    USER FLASHCARD ACTIVITY
    '''


    def add_user_flashcard_action_to_user_flashcard_activity(user_id, flashcard_id, action, dt):


        query = """INSERT INTO user_flashcard_activity(user_id, flashcard_id, flashcard_action_name, datetime) VALUES (%s, %s, %s, %s);"""
        DBServer.cur.execute(query, (user_id, flashcard_id, action, dt))
        DBServer.conn.commit()







    def get_user_flashcard_activitys_by_user_ids(user_ids):


        user_ids, = convert_to_tuple(user_ids)


        print(user_ids)

        query = """SELECT * FROM user_flashcard_activity WHERE user_id IN %s;"""
        DBServer.cur.execute(query, (user_ids, ))
        results = DBServer.cur.fetchall()

        return results

    def get_user_flashcard_activity_latest(user_id):



        query = """SELECT DISTINCT ON (user_id, flashcard_id) user_id, flashcard_id, datetime
        FROM user_flashcard_activity ORDER  BY user_id, flashcard_id, datetime DESC;"""

        DBServer.cur.execute(query, (user_id, ))
        results = DBServer.cur.fetchall()

        return results

    def format_query_args(*argv):
        # Format
        result = []
        for arg in argv:
            print(arg)

            # Format list
            if type(arg) == list:
                 arg = '(' + ''.join(ele for ele in arg) + ')'

            # Replace single quotation mark w/ double
            if type(arg) == str:
                arg = arg.replace("'", "''")

            # Append
            result.append(arg)


        return result




    def format_insert_args(*argv):
        # Format
        result = []
        for arg in argv:

            # Format list
            if type(arg) == list:
                 arg = '{' + ''.join(ele for ele in arg) + '}'

            # Replace single quotation mark w/ double
            if type(arg) == str:
                arg = arg.replace("'", "''")

            # Append
            result.append(arg)


        return result
