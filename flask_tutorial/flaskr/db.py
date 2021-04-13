
import sqlite3

import click
# g is a special object that is unique for each request.
# it store data that can be accessed by mulitple functions during the request.
# current_app is another special object that points to Flask application handling
# the request.
from flask import current_app, g
from flask.cli import with_appcontext

# the functions of this file need to be registered with application instance.
# This function takes an app and does the registration.
def init_app(app):
    # this tells the Flask to call close_db when Flask is cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # This allows us to call init_db_command with flask command.
    app.cli.add_command(init_db_command)

# get_db will be called when application starts and is handling a request.
def get_db():
    if 'db' not in g:
        # this establishes the connection to the file described by DATABASE configuratin key.
        # This file may or may not exist. It will not exist untill we intialize the database latter.
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        # sqlite3.Row tells the connection to return the rows that behave like dict.
        # This allows accessing the columns  by name.
        g.db.row_factory=sqlite3.Row
    return g.db

# a python function that will run the SQL schema
# commands we wrote in schema.sql
def init_db():
    # returns a connection to database file.
    db = get_db()
    # open_resource opens a file relative to flaskr location
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
# the click.command defines a command line command called init-db that calls the init_db function
# and shows a success message to user.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables. """
    init_db()
    click.echo('Initialized the database.')

# This method closes the connection if it exists.
# We need to tell the application in the application factory to
# call this method after each request.
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

