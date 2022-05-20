import base64
import datetime
import uuid
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from random import randrange
from neural_network.neuralClass import classify

from credentials import getCreds


def getService():
    try:
        calendar = build('calendar', 'v3', credentials=getCreds())
        return calendar

    except HttpError as error:
        print('An error occurred: %s' % error)


calendar = getService()

def createWatch():
    r = calendar.events().watch(calendarId='primary',body=
    {
  'id': str(uuid.uuid4()),
  "kind": "api#channel",
  'type': 'web_hook',
  'address': 'https://elcaptaino.duckdns.org/newEvent'
}).execute()

def newEvent(id):
    event = calendar.events().get(calendarId='primary', eventId=id).execute()
    print(event['id'])
    if isBusy(event['start']['dateTime'],event['end']['dateTime'],id):
        print('neeeeeeej')
    else:
        label = classify(event['description'])

        #createEvent(event['summery'],event['summery'],event['start']['dateTime'],event['end']['dateTime'])


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


def isBusy(timeMin, timeMax,id):
    """timeMin and timeMax are RFC3339 timestamps"""
    res = calendar.events().list(calendarId='primary',
                                 timeMin=timeMin, timeMax=timeMax).execute()
    items = res.get('items')
    print(len(items))
    if not items:
        return False

    for item in items:
        print(item['id'])
        #check if is current event/ not working correctly
        #if id==item['id']:
        #s    continue
        creator = item['creator']
        if creator.get('self') == True:
            return True

        attendees = item.get('attendees')
        if attendees:
            for a in attendees:
                if a.get('self') == True and a.get('responseStatus') == 'accepted':
                    return True
    return False


def createEvent(title,description, tag, timeMin, timeMax):
    requestBody = {
        'summary': f'[{tag}]' + title,
        'description': description,
        'start': {
            'dateTime': timeMin,
        },
        'end': {
            'dateTime': timeMax,
        }
    }
    r = calendar.events().insert(calendarId='primary', body=requestBody).execute()
    print(r)


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

def main(network_response):
    if isBusy(network_response['timeMin'],network_response['timeMax']):
        #skriv en mail retur vi ikke kan
        print('nej')
        return False
    else:
        createEvent(**network_response)
        #lave et eller andet der bekræfter vi har fået noget i kalenderen.
        #skriv email til sender at vi kan
        return True
      
if __name__ == '__main__':
    network_response = {
        'title': 'Title on event',
        'description': 'Selve email tekst',
        'tag': 'social',  # social/business
        'timeMin': '2022-05-15T13:00:00+02:00',
        'timeMax': '2022-05-15T16:30:00+02:00'
    }
    #main(network_response)
    createWatch()
    newEvent('7n7qkonu905k92d35u1n8veah4')
  
    
