#!/usr/bin/python3
"""
People API Contacts Module
"""
import requests
from google.auth import credentials

# Set the credentials path to the downloaded JSON file
credentials_path = './credentials.json'

# Create credentials object from the JSON file
creds = credentials.Credentials.from_authorized_user_file(credentials_path)
creds.refresh(requests.Request())

# Define the contact name to search
contact_name_to_search = 'John Doe'  # Replace this with the name you want to search

# Define the base URL for the People API
base_url = 'https://people.googleapis.com/v1/otherContacts:search'

# Construct the request payload
params = {
    'query': contact_name_to_search,
    'readMask': 'names,emailAddresses',  # Define the fields you want to retrieve
}

# Make the API request
response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {creds.token}'})
if response.status_code == 200:
    # Process the response
    data = response.json()
    contacts = data.get('otherContacts', [])
    if contacts:
        for contact in contacts:
            names = contact.get('names', [])
            if names:
                print(f"Contact found: {names[0].get('displayName')}")
            else:
                print("No name found for this contact.")
    else:
        print("No contacts found.")
else:
    print(f"Failed to fetch contacts. Status code: {response.status_code}")
    print(response.text)  # Print the error response if any
