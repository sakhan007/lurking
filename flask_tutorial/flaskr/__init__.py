"""
The __init__.py does two duties.
    1. contains application factory
    2. tells python that flaskr directory should be treated as a python package.
"""


import os
from flask import Flask

def create_app(test_config=None):
    # create the Flask instance, __name__ is the name of current module.
    # the app needs to know the name to setup some paths.
    # the instance_relative_config=True tells the app that the configuration files
    # are relative to the instance folder. The instance folder will be outside flaskr directory
    # and should not be commited to version control, as it contains local data such as configuration secrets and database file.
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping will set some default configuration that the app will use.
    # SECRET_KEY is used by Flask to keep data safe. The chosen 'dev' should be changed when
    # deploying the project.
    # DATABASE is the path where sqlite database will be saved. app.instance_path is the path
    # chosen by Flask for its instance folder.
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )
    # This overrides default values with the values from config.py file in the instance folder
    # if it exists.
    # For example, when deploying here we can set the real SECRET_KEY
    # test_config is the just test configuration file that tests various configuartion
    # independently of the actual deployment configuration.

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    # Flask does not create instance folder automatically but it is required since sqlite
    # file will be created there.
    try:
        os.mkdirs(app.instance_path)
    except OSError:
        pass
    # This is how a simple route is created so that we can see the application working.
    # it creates a connection between the URL /hellow and a function that returns a response, the string 'hello, world!' in this case.
    # simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app
