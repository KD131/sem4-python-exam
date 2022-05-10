import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json

from credentials import getCreds

def getService():
    try:
        gmail = build('gmail', 'v1', credentials=getCreds())
        return gmail
        
    except HttpError as error:
        print('An error occurred: %s' % error)


gmail = getService()

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

def getAllMails():
    # Prints plaintext content of all mails
    # If we return a list of more than 100, we might want to up the maxResults param. If more than 500, we need list_next().
    mails_response = gmail.users().messages().list(userId='me').execute()
    mails = mails_response['messages']
    
    for m in mails:
        actual_mail = gmail.users().messages().get(userId='me', id=m['id']).execute()
        message = getPlainText(actual_mail)
        print(message)

def createWatch():
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/exam-project-349112/topics/exam-project-349112-topic'
        }

    r = gmail.users().watch(userId='me', body=request).execute()
    return r

def getEmailsFromHistory(history_id):
    res = gmail.users().history().list(userId='me', startHistoryId=history_id).execute()
    # message_ids = [message['id'] for message in history['messages'] for history in res['history']]
    history = res.get('history')
    if history:
        message_ids = []
        for hist in history:
            for message in hist['messages']:
                message_ids.append(message['id'])
        
        messages = []
        for id in message_ids:
            mail = gmail.users().messages().get(userId='me', id=id).execute()
            messages.append(getPlainText(mail))

    return res, messages

if __name__ == '__main__':
    # 2522
    # 2472
    print(json.dumps(getEmailsFromHistory(2581), indent=4))
