from flask import Flask
import random
import string
import os


def create_app():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(100))

    app = Flask(__name__)
    app.config['SECRET_KEY'] = password
    app.config['DOWNLOAD_DIRECTORY'] = os.environ.get('FLASK_DOWNLOAD_DIRECTORY') + '/'
    if app.config['DOWNLOAD_DIRECTORY'] == "" or app.config['DOWNLOAD_DIRECTORY'] is None:
        app.config['DOWNLOAD_DIRECTORY'] = '/'
    app.config['LEN_DOWNLOAD_DIRECTORY'] = app.config['DOWNLOAD_DIRECTORY'].count('/')
    print("Current download directory is ", app.config['DOWNLOAD_DIRECTORY'])
# 7 + 1

    from .views import views
    from .download import download

    app.register_blueprint(download, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
