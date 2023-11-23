#!/usr/bin/python3
"""
Authentication Module
"""
from dotenv import load_dotenv
from flask import Blueprint, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
import jwt
from os import getenv
import requests
from models.user import User

# Load environment variables
load_dotenv()

# Create auth blueprint
auth = Blueprint('auth', __name__)


@auth.route('/user/login', methods=['GET'], strict_slashes=False)
def login():
    """ Login """

    # Get code from query string
    code = request.args.get('code')

    # Get ID and Access tokens using code
    tokens_url = getenv('GOOGLE_GET_TOKENS_URL')

    query_params = {
        'code': code,
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': getenv('GOOGLE_REDIRECT_URI'),
        'grant_type': 'authorization_code'
    }
    query_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    tokens_response = requests.post(tokens_url, params=query_params, headers=query_headers)
    
    id_token = tokens_response.json().get('id_token')
    # access_token = tokens_response.json().get('access_token')
    refresh_token = tokens_response.json().get('refresh_token')
    # expires_in = tokens_response.json().get('expires_in')

    # Get the user details from the ID token
    google_user = jwt.decode(jwt=id_token, options={"verify_signature": False})

    # Create and save user document in db
    new_user = User(
        first_name=google_user.get('given_name'),
        last_name=google_user.get('family_name'),
        email=google_user.get('email'),
        refresh_token=refresh_token
    )
    new_user.save()
    print()
    print(new_user)

    # Save user in Flask session
    login_user(new_user)

    return redirect(url_for('logged_in'))    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))