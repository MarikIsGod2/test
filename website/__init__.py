from flask import Flask
import random
import string
import subprocess
import os
def create_app():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(100))

    app = Flask(__name__)
    app.config['SECRET_KEY'] = password
    app.config['DOWNLOAD_DIRECTORY'] = '/mnt/c/Users/Support/Desktop/web_file_explorer_python/download_folder/'
    print("Current download directory is "+app.config['DOWNLOAD_DIRECTORY'])

    from .views import views
    from .download import download

    print(os.getenv("FLASK_DOWNLOAD_DIRECTORY"))

    app.register_blueprint(download, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app