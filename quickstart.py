from __future__ import print_function
import base64

import datetime
import json
import os.path
from calendar import calendar

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://mail.google.com/']

event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2022-05-03T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2022-05-04T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        gmail = build('gmail', 'v1', credentials=creds)
        global event


        #create a test event.
        #service.events().insert(calendarId='primary',body=event).execute()


        #check if busy
        busyRequest= {
            "timeMin": "2022-05-02T09:00:00-07:00",
            "timeMax": "2022-05-04T09:00:00-07:00",
            "groupExpansionMax": 50,
            "calendarExpansionMax": 50,
            "items": [
                 {
                 "id":'primary'
                 }
             ]
        }

        #check if busy. No event description Det er shit, vi skal ikke bruge den.
        reponse = service.freebusy().query(body=busyRequest).execute()
        #print(reponse)


        #find busy by events.list(). returns list of event in time interval.
        eventCheck = service.events().list(calendarId='primary',timeMin="2022-05-03T09:00:00-07:00",timeMax='2022-05-04T17:00:00-07:00').execute()
        print(eventCheck)



        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


        # Prints plaintext content of all mails
        # If we return a list of more than 100, we might want to up the maxResults param. If more than 500, we need list_next().
        mails_response = gmail.users().messages().list(userId='me').execute()
        mails = mails_response['messages']
        m = mails[0]
        # for m in mails:
        actual_mail = gmail.users().messages().get(userId='me', id=m['id']).execute()
        print(json.dumps(actual_mail, indent=4))
        parts = actual_mail['payload']['parts']
        # We can iterate through the parts and find the right one, or we can just say that the plain text is always the first element.
        # If we iterate, it'd be something like checking partId == '0', mimeType == 'text/plain', even iterating through headers and finding name == 'Content-Type' and value == 'text/plain; charset=\"UTF-8\"'
        # Basically, there's a lot more validation we can do, but is probably not needed.
        # Actually, I think we need to recursively dig to find the plain text. Oof.
        data = parts[0]['body']['data']
        message = base64.b64decode(data.encode()).decode()
        print(message)

    except HttpError as error:
        print('An error occurred: %s' % error)
        


if __name__ == '__main__':
    main()


