# Imports

# Python standard library
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




class SQLServer(object):


    # Postgres settings
    dbname = 'flashy'
    username = 'prestonh'
    password = 'password'

    engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
    print(engine.url)

    ## create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)
    print('database load:', database_exists(engine.url))

    # Create tables (if they do not exist)

    conn = psycopg2.connect(f"dbname={dbname} user={username} host='localhost' password={password}")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)




    table_names = ['users', 'flashcards', 'user_flashcard_relations', 'user_site_activity', 'user_flashcard_activity']
    for table_name in table_names:
        cur.execute(f"""SELECT COUNT(*) FROM {table_name} LIMIT 1;""")
        print(table_name, cur.fetchall())



    def get_user_by_email(email):
        # Insert into table
        query = f"""SELECT * FROM users WHERE email = '{email}';"""
        SQLServer.cur.execute(query)
        user = SQLServer.cur.fetchone()
        return user




    def add_user_to_users(email, password, name):



        # Date created
        date_created = datetime.datetime.now()

        # Insert into table
        query = """INSERT INTO users(email, password, name, date_created) VALUES (%s, %s, %s, %s) RETURNING user_id;"""
        SQLServer.cur.execute(query, (email, password, name, date_created))
        SQLServer.conn.commit()
        user_id = SQLServer.cur.fetchone()['user_id']

        return user_id


    def add_flashcard_to_flashcards(front, back):

        # Format
        front, back = SQLServer.format_query_args(front, back)


        # Insert into table
        query = """INSERT INTO flashcards(front, back) VALUES (%s, %s) RETURNING flashcard_id;"""
        SQLServer.cur.execute(query, (front, back))

        SQLServer.conn.commit()
        flashcard_id = SQLServer.cur.fetchone()['flashcard_id']
        return flashcard_id

    def add_user_flashcard_to_user_flashcard_relations(user_id, flashcard_id, labels):
        # Insert into table
        user_id, flashcard_id, labels = SQLServer.format_query_args(user_id, flashcard_id, labels)

        query = """INSERT INTO user_flashcard_relations(user_id, flashcard_id, labels) VALUES (%s, %s, %s);"""
        SQLServer.cur.execute(query, (user_id, flashcard_id, labels));
        SQLServer.conn.commit()

    def add_user_flashcard_action_to_user_flashcard_activity(user_id, flashcard_id, action):

        user_id, flashcard_id, activity = SQLServer.format_query_args(user_id, flashcard_id, labels)
        query = """INSERT INTO user_flashcard_activity(user_id, flashcard_id, action) VALUES (%s, %s, %s);"""
        SQLServer.cur.execute(query, (user_id, flashcard_id, activity))
        SQLServer.cur.commit()






    def get_flashcards_by_user_id(user_id):
        query = f"""SELECT * FROM flashcards WHERE flashcard_id IN \
                    (SELECT flashcard_id, labels FROM user_flashcard_relations LEFT JOIN users \
                    ON (user_flashcard_relations.user_id = users.user_id) WHERE users.user_id = {user_id});"""


        query = f"""SELECT * FROM flashcards LEFT JOIN user_flashcard_relations ON \
            (flashcards.flashcard_id = user_flashcard_relations.flashcard_id) WHERE \
            user_flashcard_relations.user_id = {user_id};"""



        SQLServer.cur.execute(query);
        flashcards = SQLServer.cur.fetchall()


        return flashcards



    def format_query_args(*argv):
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
