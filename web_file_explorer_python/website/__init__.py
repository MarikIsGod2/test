from flask import Flask
import random
import string

def create_app():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(50))

    app = Flask(__name__)
    app.config['SECRET_KEY'] = password

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app
