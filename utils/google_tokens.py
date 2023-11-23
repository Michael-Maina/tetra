#!/usr/bin/python3
"""
Google Tokens Helper Module
"""
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

def refresh(refresh_token):
    """
    Refreshes access_token if expired using the refresh_token

    args: token - refresh_token(valid for 365 days)
    return: access_token - fresh access_token(valid for 1 hour)
    """

    base_url = getenv('GOOGLE_GET_TOKENS_URL')
    query_params = {
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    query_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(base_url, params=query_params, headers=query_headers)

    access_token = response.json().get('access_token')
    return access_token

def get_google_user(access_token):
    """
    Accesses user data using the access_token

    args: token - access_token
    return: user data
    """
    user_data_uri = getenv('GOOGLE_LOGIN_URI')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'alt': 'json',
        'access_token': access_token
    }
    response = requests.get(user_data_uri, params=params, headers=headers)

    if response.status_code == 401:
        return {'status': 'expired'}
    elif response.status_code != 200:
        return {}
    else:
        return {'status': 'OK'}
