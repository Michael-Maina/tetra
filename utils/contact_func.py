#!/usr/bin/python3
"""
People API Contacts Module
"""
from dotenv import load_dotenv
from flask_login import current_user
from os import getenv
import requests
from utils.google_tokens import refresh


# Load environment variables
load_dotenv()


def get_user_contact(search_query, access_token):
    """
    Searches contact using Google's People API

    args: search_query - contact to search
    return: list of contacts found matching query
    """

    # Define the base URL for the People API
    base_url = getenv('PEOPLE_API_BASE_URI')

    # Request payload
    params = {
        'query': search_query,
        'readMask': 'names,emailAddresses',  # Define the fields you want to retrieve
    }

    # Make the API request
    response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {access_token}'})
    contacts_list = []
    contact = {}

    if response.status_code == 401:
        access_token = refresh(current_user.refresh_token)
        response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {access_token}'})

    if response.status_code == 200:
        # Process the response
        data = response.json()
        results = data.get('results', [])

        if results:
            for result in results:
                person = result.get('person')
                names = person.get('names')
                emails = person.get('emailAddresses')

                if names:
                    contact['name'] = names[0].get('displayName')
                    print(f"Contact found: {names[0].get('displayName')}")
                else:
                    print("No name found for this contact.")

                if emails:
                    contact['email'] = emails[0].get('value')
                    print(f"Contact found: {emails[0].get('value')}")
                else:
                    print("No email found for this contact.")
                
                contacts_list.append(contact)                

        else:
            print("No contacts found.")
    else:
        print(f"Failed to fetch contacts. Status code: {response.status_code}")
        print(response.text)

    return contacts_list
