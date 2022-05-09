from __future__ import print_function
import base64


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer

import datetime
from email import message
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
    #Downloads the differents nltk packages. outcomment first time to download them. 
    #nltk.download('punkt')
    #nltk.download('stopwords')
    #nltk.download('wordnet')
    #nltk.download('averaged_perceptron_tagger') # for POS_tag
    #nltk.download('maxent_ne_chunker') # for NER
    #nltk.download('words')

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
        
        for m in mails:
            actual_mail = gmail.users().messages().get(userId='me', id=m['id']).execute()
            message = getPlainText(actual_mail)
            print(message)

    except HttpError as error:
        print('An error occurred: %s' % error)
        

# Can be refactored to take the target type as a parameter, i.e. getContent(mail, target='text/plain').
# This would allow you to search for something else like html if needed
def getPlainText(mail):
    payload = mail['payload']

    def recurse(part):
        """Depth-First Search (DFS).
        Takes an element containing a mimeType attribute, such as the payload of the email and any sub-parts.
        """
        mime_type = part['mimeType']
        if mime_type == 'text/plain':
            return part['body']['data']
        elif mime_type.startswith('multipart'):
            for p in part['parts']:
                res = recurse(p)
                if res:
                    return res
        else:
            return None

    data = recurse(payload)
    message = base64.urlsafe_b64decode(data.encode()).decode()
    return message


#Trying to make nltk work.
text = "Hello, my name isn't Kasper but August. CAN YOU believe that? I am born in 1993."


def cleaningText(text):
    #Tokenizes the text
    tokens = word_tokenize(text)
    tokens = list(map(str.lower,tokens))

    #if we want to remove stopwords ("this, and , are , is")
    #stop_words = set(stopwords.words('english'))
    #tokens = [w for w in tokens if not w in stop_words]

    #stemming the text with PorterStemmer
    #This init the stemmer.
    #stemmer = PorterStemmer()
    #words=["connect","connected","connection","connections","connects","house","housing"] #Word to see if the stemmer is working 
    #stemmed_words = [stemmer.stem(word=word) for word in tokens]
    #print(stemmed_words)

    #stemming the text with SnowballStemmer this is in general better, and can take different language as danish!
    #Init the stemmer
    #sn_stemmer = SnowballStemmer("english") # Can be change to danish
    #words=["connect","connected","connection","connections","connects","house","housing"] #Word to see if the stemmer is working 
    #stemmed_words = [sn_stemmer.stem(word=word) for word in tokens]
    #print(stemmed_words)

    #Lemmatization considers the context and converts the word to its meaningful base form, which is called Lemma. Sometimes, the same word can have multiple different Lemmas
    #Init the lemma.
    #lemmatizer = WordNetLemmatizer()
    #words=["trouble","troubling","troubled","troubles"] #Words to see if the lemma is working. 
    #lemmatized_words= [lemmatizer.lemmatize(word=word,pos='v') for word in tokens]
    #print(lemmatized_words)

    return tokens

textUpdated = cleaningText(text)

print(textUpdated)


if __name__ == '__main__':
    main()


