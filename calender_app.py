import json
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
# import datetime
from datetime import datetime, timedelta



# Disable OAuthlib's HTTPs verification when running locally.
# This is only for testing purposes!
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.secret_key = "Alstede2480"  # Replace with a strong secret key

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# This should be set to your web app's URL
REDIRECT_URI = "http://localhost:5000/oauth2callback"

# The client_secrets.json file downloaded from the Google Cloud Console
CLIENT_SECRETS = "Cred2.json"




@app.route("/")
def home():
    if "credentials" not in session:
        return redirect(url_for("login"))

    # Load the credentials from the JSON string
    credentials_info = json.loads(session["credentials"])

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

    print(events)
    if not events:
        return "No upcoming events found."

    upcoming_events = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        upcoming_events.append({"start": start, "summary": event["summary"], "id": event["id"]})

    return render_template("home.html", upcoming_events=upcoming_events)


@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS, SCOPES, redirect_uri=REDIRECT_URI)
    authorization_url, state = flow.authorization_url(prompt="consent")

    # Store the state so the callback can verify the response.
    session["oauth_state"] = state

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session["oauth_state"]

    flow = Flow.from_client_secrets_file(CLIENT_SECRETS, SCOPES, state=state, redirect_uri=REDIRECT_URI)
    flow.fetch_token(authorization_response=request.url)

    # Store the credentials in the session.
    credentials = flow.credentials
    session["credentials"] = credentials.to_json()

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    # print(session["credentials"])
    session.pop("credentials", None)
    return redirect(url_for("login"))

@app.route("/create")
def create():

    # Load the credentials from the JSON string
    credentials_info = json.loads(session["credentials"])

    credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)
    service = build("calendar", "v3", credentials=credentials)

    event = {
        'summary': 'Test Event',
        'description': 'This is a test event.',
        'start': {
            'dateTime': (datetime.now() + timedelta(days=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': False,  # Set to False to use custom reminders
            'overrides': [
                {'method': 'popup', 'minutes': 10},  # Notify 10 minutes before the event
                {'method': 'email', 'minutes': 30},  # Notify 30 minutes before the event via email
            ],
        },
    }
    service.events().insert(calendarId="dmurage140@gmail.com", body=event).execute()
    return redirect(url_for("home"))

@app.route("/delete/<event_id>", methods=["DELETE"])
def delete(event_id):
    if "credentials" not in session:
        return redirect(url_for("login"))

    # Load the credentials from the JSON string
    credentials_info = json.loads(session["credentials"])

    credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)
    service = build("calendar", "v3", credentials=credentials)

    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        # return jsonify({"status": "success", "message": "Event deleted successfully"})
        return redirect(url_for("home"))
    except HttpError as error:
        return jsonify({"status": "error", "message": f"Error deleting event: {error}"})


if __name__ == "__main__":
    app.run(debug=True)


