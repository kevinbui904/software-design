'''
    disney-api.py
    Authors: Kevin Bui, Robbie Young, November 11 2021
    * add desc of doc
    For use in the final project in Carleton College's CS 257 Software Design Class, Fall 2021
'''


import flask
import json
import psycopg2
import argparse
import config
from config import database as config_database
from config import user as config_user
from config import password as config_password

api = flask.Blueprint('api', __name__)


def connect(connect_database, connect_user, connect_password):
    try:
        connection = psycopg2.connect(
            database=connect_database, user=connect_user, password=connect_password)
        return connection
    except Exception as e:
        print(e)
        exit()


def create_list(cursor):
    content_list = []

    for this_content in cursor:
        this_dict = {}
        this_dict['type'] = this_content[0]
        this_dict['title'] = this_content[1]
        this_dict['directors'] = this_content[2]
        this_dict['cast'] = this_content[3]
        this_dict['date_added'] = this_content[4]
        this_dict['release_year'] = this_content[5]
        this_dict['rating'] = this_content[6]
        this_dict['duration'] = this_content[7]
        this_dict['listed_in'] = this_content[8]
        this_dict['description'] = this_content[9]
        content_list.append(this_dict)

    return content_list


@api.route('/')
def hello():
    return 'Isitondisney.com'


@api.route('/recommended')
def genre():
    connection = connect(config_database, config_user, config_password)
    genre = flask.request.args.get('genre')

    genre_formatted = "%" + genre + "%"
    query = '''SELECT type, title, director, actors, date_added, release_year, rating, duration, genres, description
                FROM countries, date_added, genres, rating, super_table, type
                WHERE super_table.countries_id = countries.id
                AND super_table.date_added_id = date_added.id
                AND super_table.genres_id = genres.id
                AND super_table.rating_id = rating.id
                AND super_table.type_id = type.id'''

    try:
        cursor = connection.cursor()

        query = query + ''' AND LOWER(genres.genres) LIKE LOWER(%s)
                    ORDER BY RANDOM()
                    LIMIT 1;'''
        cursor.execute(query, (genre_formatted, ))

    except Exception as e:
        connection.close()
        print(e)
        exit()

    content_list = create_list(cursor)
    connection.close()
    return json.dumps(content_list)

# * for genre, to keep the scope of this project simple, the only genre they could select from is "action", "comedy", "documentary", "sci-fi"


@api.route('/directors/<directors_name>')
def director(directors_name):
    connection = connect(config_database, config_user, config_password)
    director_formatted = "%" + directors_name + "%"
    query = '''SELECT type, title, director, actors, date_added, release_year, rating, duration, genres, description
                FROM countries, date_added, genres, rating, super_table, type
                WHERE super_table.countries_id = countries.id
                AND super_table.date_added_id = date_added.id
                AND super_table.genres_id = genres.id
                AND super_table.rating_id = rating.id
                AND super_table.type_id = type.id
                AND LOWER(super_table.director) LIKE LOWER(%(directors_name)s)
                ORDER BY title;
                '''

    try:
        cursor = connection.cursor()
        cursor.execute(
            query, {'directors_name': director_formatted})

    except Exception as e:
        connection.close()
        print(e)
        exit()

    content_list = create_list(cursor)
    connection.close()
    return json.dumps(content_list)
# * let's restrict searches ONLY to 1 author at a time


@api.route('/titles/<titles_string>')
def titles(titles_string):
    connection = connect(config_database, config_user, config_password)
    title_formatted = "%" + titles_string + "%"
    query = '''SELECT type, title, director, actors, date_added, release_year, rating, duration, genres, description
                FROM countries, date_added, genres, rating, super_table, type
                WHERE super_table.countries_id = countries.id
                AND super_table.date_added_id = date_added.id
                AND super_table.genres_id = genres.id
                AND super_table.rating_id = rating.id
                AND super_table.type_id = type.id
                AND LOWER(super_table.title) LIKE LOWER(%(title)s)
                ORDER BY title;
                '''

    try:
        cursor = connection.cursor()
        cursor.execute(
            query, {'title': title_formatted})

    except Exception as e:
        connection.close()
        print(e)
        exit()

    content_list = create_list(cursor)
    connection.close()
    return json.dumps(content_list)


@api.route('/cast/<cast_name>')
def cast(cast_name):
    connection = connect(config_database, config_user, config_password)
    cast_formatted = "%" + cast_name + "%"
    query = '''SELECT type, title, director, actors, date_added, release_year, rating, duration, genres, description
                FROM countries, date_added, genres, rating, super_table, type
                WHERE super_table.countries_id = countries.id
                AND super_table.date_added_id = date_added.id
                AND super_table.genres_id = genres.id
                AND super_table.rating_id = rating.id
                AND super_table.type_id = type.id
                AND LOWER(super_table.actors) LIKE LOWER(%(cast_name)s)
                ORDER BY title;
                '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, {'cast_name': cast_formatted})
    except Exception as e:
        connection.close()
        print(e)
        exit()

    content_list = create_list(cursor)
    connection.close()
    return json.dumps(content_list)
# * let's restrict searches ONLY to 1 cast at a time


def main():
    parser = argparse.ArgumentParser(
        'Flask application for the disney web application')
    parser.add_argument(
        'host', help='the host on which this application is running')
    parser.add_argument(
        'port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    api.run(host=arguments.host, port=arguments.port, debug=True)


if __name__ == '__main__':
    main()
