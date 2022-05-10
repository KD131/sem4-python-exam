import base64
import datetime
import json
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


def isBusy(timeMin, timeMax):
    """timeMin and timeMax are RFC3339 timestamps"""
    res = calendar.events().list(calendarId='primary',timeMin=timeMin,timeMax=timeMax).execute()
    items = res.get('items')
    if not items:
        return False
    
    for item in items:
        creator = item['creator']
        if creator.get('self') == True:
            return True
        
        attendees = item.get('attendees')
        if attendees:
            for a in attendees:
                if a.get('self') == True and a.get('responseStatus') == 'accepted':
                    return True
    return False

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

if __name__ == '__main__':
    network_response = {
        'timeMin': '2022-05-3T13:00:00+02:00',
        'timeMax': '2022-05-10T16:30:00+02:00'
    }
    # res = isBusy(network_response['timeMin'], network_response['timeMax'])
    res = isBusy(**network_response)
    print(res)

