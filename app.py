#!/usr/bin/python3
"""
Simple REST API Module
"""
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_login import LoginManager, login_required
from models.user import User
from os import getenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')

# Flask-Login init
login_manager = LoginManager()
login_manager.init_app(app)

# Register blueprint for auth routes
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Landing Page """
    return render_template('landing.html')

@app.route('/user', methods=['GET'], strict_slashes=False)
@login_required
def logged_in():
    """ Testing Login """
    return render_template('logged_in.html')


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


if __name__ == '__main__':
    API_HOST = getenv('API_HOST')
    API_PORT = getenv('API_PORT')

    host = API_HOST if API_HOST else '0.0.0.0'
    port = API_PORT if API_PORT else 5000

    app.run(port=port, host=host, debug=True)
