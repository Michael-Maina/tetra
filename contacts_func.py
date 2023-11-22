#!/usr/bin/python3
"""
People API Contacts Module
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Set the credentials path to the downloaded JSON file
credentials_path = './credentials.json'

# Create credentials object from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/contacts.readonly']
)

# Build the People API service
service = build('people', 'v1', credentials=credentials)

def search_contact_by_name(name):
    # Define the query for searching contacts by name
    query = f'names:{name}'

    # Make an API request to search for contacts
    results = service.people().connections().list(
        resourceName='people/me',
        personFields='names',
        pageSize=10,
        sortOrder='LAST_MODIFIED_DESCENDING',
        query=query
    ).execute()

    # Process the results
    contacts = results.get('connections', [])
    if contacts:
        for contact in contacts:
            names = contact.get('names', [])
            if names:
                print(f"Contact found: {names[0].get('displayName')}")
            else:
                print("No name found for this contact.")
    else:
        print("No contacts found.")

# Search for a specific contact by name
contact_name_to_search = 'John Doe'  # Replace this with the name you want to search
search_contact_by_name(contact_name_to_search)
