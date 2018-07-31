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
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)



    table_names = ['users', 'flashcards', 'user_collection', 'user_site_activity', 'user_flashcard_activity']
    for table_name in table_names:
        cur.execute(f"""SELECT COUNT(*) FROM {table_name} LIMIT 1;""")
        print(table_name, cur.fetchone()[0])



    def get_cur():
        return SQLServer.cur


    def get_user_by_email(email):
        # Insert into table
        query = f"""SELECT * FROM users WHERE email = '{email}';"""
        SQLServer.cur.execute(query)
        user = SQLServer.cur.fetchone()
        return user




    def add_user(email, password, name):



        # Date created
        date_created = datetime.datetime.now()

        # Insert into table
        query = f"""INSERT INTO users(email, password, name, date_created) VALUES ('{email}', '{password}', '{name}', '{date_created}')"""
        SQLServer.cur.execute(query)
        SQLServer.conn.commit()
        return True


    def insert_flashcard(front, back, labels):

        # Format
        front, back, labels = format_query_args(front, back, labels)

        # Check SQL injection
        front, back, labels = validate_safe_SQL(front, back, labels)

        # Insert into table
        query = f"""INSERT INTO flashcards(front, back, labels) VALUES ('{front}', '{back}', '{labels}')"""
        SQLServer.cur.execute(query)
        SQLServer.conn.commit()

        labels = '{' + ''.join(label for label in labels) + '}'

    def load_all_flashcards():

        query = f"""SELECT * FROM flashcards;""";
        SQLServer.cur.execute(query)
        flashcards = SQLServer.cur.fetchall()

        formatted_flashcards = []
        for flashcard in flashcards:
            formatted_flashcard = {}
            formatted_flashcard['front'] = flashcard['front']
            formatted_flashcard['back'] = flashcard['back']
            formatted_flashcard['id'] = flashcard['card_id']
            formatted_flashcard['label'] = flashcard['labels']
            formatted_flashcards.append(formatted_flashcard)


        return formatted_flashcards



    def format_query_args(*argv):
        # Format
        result = []
        for arg in argv:

            # Format list
            if type(arg) == list:
                 arg = '{' + ''.join(ele for ele in arg) + '}'

            # Replace single quotation mark w/ double
            arg = arg.replace("'", "''")

            # Append
            result.append(arg)


        return result




    def validate_safe_SQL(*argv):
        return argv
