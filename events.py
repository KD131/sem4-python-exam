import base64
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from credentials import getCreds

def getService():
    try:
        calendar = build('calendar', 'v3', credentials=getCreds())
        return calendar
        
    except HttpError as error:
        print('An error occurred: %s' % error)


calendar = getService()

def getUpcoming():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = calendar.events().list(calendarId='primary', timeMin=now,
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


def checkBusy(timeMin, timeMax):
    """timeMin and timeMax are datetimes"""
    res = calendar.events().list(calendarId='primary',timeMin=timeMin,timeMax=timeMax).execute()
    return res

def createEvent(event):
    calendar.events().insert(calendarId='primary',body=event).execute()

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

