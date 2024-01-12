import json
from flask import Blueprint, Flask, render_template, redirect, request, url_for, session, jsonify
from flask_login import current_user, login_required
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from uuid import uuid4
from models.event import Event



# Create auth blueprint
calendar = Blueprint('calendar', __name__)

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/contacts.other.readonly',
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.events']


# The client_secrets.json file downloaded from the Google Cloud Console
CLIENT_SECRETS = "credentials.json"


@calendar.route("/calendar")
@login_required
def home():

    # Load the credentials from the JSON string
    credentials_info = {
        'token': current_user.access_token,
        'refresh_token': current_user.refresh_token,
        'token_uri': getenv('GOOGLE_GET_TOKENS_URL'),
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'scopes': SCOPES
    }

    credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)


    service = build("calendar", "v3", credentials=credentials)

    now = datetime.utcnow().isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    for event in events:
        print()
        print(event)
        print()

    if not events:
        return "No upcoming events found."

    upcoming_events = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        upcoming_events.append({"start": start, "summary": event["summary"], "id": event["id"]})

    # print(upcoming_events)
    return render_template("home.html", upcoming_events=upcoming_events)


@calendar.route("/create")
@login_required
def create():

    # Load the credentials from the JSON string
    credentials_info = credentials_info = {
        'token': current_user.access_token,
        'refresh_token': current_user.refresh_token,
        'token_uri': getenv('GOOGLE_GET_TOKENS_URL'),
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'scopes': SCOPES
    }

    credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)
    service = build("calendar", "v3", credentials=credentials)

    event = {
        'summary': 'Test Event',
        'description': 'This is a test event.',
        'conferenceDataVersion': 1,

        'start': {
            'dateTime': (datetime.now() + timedelta(days=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
                {'method': 'email', 'minutes': 30},
            ],
        },

        'attendees': [{
            'email': "dmurage140@gmail.com"
        }],

        'conferenceData': {
            'createRequest': {
                "requestId": str(uuid4()),
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
    }

    new_event = service.events().insert(calendarId=current_user.email, body=event, sendUpdates="all", conferenceDataVersion=1).execute()

    # db_event = Event(

    # )

    print("New event: ")
    print(new_event)

    return redirect(url_for("calendar.home"))


@calendar.route("/delete/<event_id>")
@login_required
def delete(event_id):

    # Load the credentials from the JSON string
    credentials_info =  {
        'token': current_user.access_token,
        'refresh_token': current_user.refresh_token,
        'token_uri': getenv('GOOGLE_GET_TOKENS_URL'),
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'scopes': SCOPES
    }

    credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)
    service = build("calendar", "v3", credentials=credentials)

    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return redirect(url_for("calendar.home"))
    except HttpError as error:
        return jsonify({"status": "error", "message": f"Error deleting event: {error}"})
