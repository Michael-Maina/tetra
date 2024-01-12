#!/usr/bin/python3
"""
Authentication Module
"""
from dotenv import load_dotenv
from flask import Blueprint, request, redirect, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from utils.google_tokens import *
import jwt
from models.user import User
from os import getenv
import requests

# Load environment variables
load_dotenv()

# Create auth blueprint
auth = Blueprint('auth', __name__)


@auth.route('/user/signup', methods=['GET'], strict_slashes=False)
def signup():
    """ Signup """

    # Get code from query string
    code = request.args.get('code')

    # Get ID and Access tokens using code
    tokens_url = getenv('GOOGLE_GET_TOKENS_URL')

    query_params = {
        'code': code,
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': getenv('GOOGLE_SIGNUP_REDIRECT_URI'),
        'grant_type': 'authorization_code'
    }
    query_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    tokens_response = requests.post(tokens_url, params=query_params, headers=query_headers)

    id_token = tokens_response.json().get('id_token')
    access_token = tokens_response.json().get('access_token')
    refresh_token = tokens_response.json().get('refresh_token')

    print(id_token)
    print("access_token:")
    print(access_token)
    print("refresh_token:")
    print(refresh_token)

    # Get the user details from the ID token
    google_user = jwt.decode(jwt=id_token, options={"verify_signature": False})

    try:
        user = User.objects.get(email=google_user.get('email')) # if this returns a user, then the email already exists in database

        # if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.login'))

    except User.DoesNotExist:
        # Create and save user document in db
        new_user = User(
            first_name=google_user.get('given_name'),
            last_name=google_user.get('family_name'),
            email=google_user.get('email'),
            access_token=access_token,
            refresh_token=refresh_token,
            authenticated=True
        )
        new_user.save()

        # Save user object in Flask session
        login_user(new_user, remember=True)
        session['credentials'] = tokens_response.json()

        return redirect(url_for('logged_in'))


@auth.route('/user/login', methods=['GET'], strict_slashes=False)
def login():
    """ Login """

    user = current_user
    if user.is_authenticated:
        return redirect(url_for('logged_in'))

    print(session["credentials"])
    if session.get('credentials').get('expires_in') <= 0:
        new_token = refresh(user.refresh_token)
        session['credentials']['access_token'] = new_token
        user.access_token = new_token

    user_data = get_google_user(user.access_token)
    if not user_data:
        return redirect(url_for('signup'))
    elif user_data.get('status') == 'expired':
        new_token = refresh(user.refresh_token)
        user.access_token = new_token

    user.authenticated = True
    login_user(user, remember=True)
    return redirect(url_for('logged_in'))


@auth.route('/logout', methods=['GET'], strict_slashes=False)
@login_required
def logout():
    """ Logout """

    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('index'))
