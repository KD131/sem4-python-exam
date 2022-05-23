import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    messages = []
    if history:
        message_ids = []
        for hist in history:
            for message in hist['messages']:
                message_ids.append(message['id'])
        
        
        for id in message_ids:
            mail = gmail.users().messages().get(userId='me', id=id).execute()
            mail_body = getPlainText(mail)
            mail_subject = get_header('Subject', mail)
            # can be refactored to a dict or just return mail and call the get methods from server.py
            messages.append((mail_subject, mail_body, mail))

    return res, messages

def get_header(header, mail):
    payload = mail['payload']
    headers = payload['headers']
    for h in headers:
        if h['name'] == header:
            return h['value']

def get_thread_id(mail):
    return mail['threadId']


def isSpam(body):
    spamString = '''Forwarding this invitation could allow any recipient to send a response to'''
    if body != None and spamString in body:
        return True
    else:
        return False

def send_mail(body, to=None, subject=None, reply_to=None):
    if not (to or reply_to):
        raise Exception("Must have recipient either as to= or be a reply")
    if not (subject or reply_to):
        raise Exception("Must have subject either as subject= or be a reply")

    message = MIMEText(body)
    mail = {}

    if reply_to:
        to = get_header('Return-Path', reply_to)
        subject = get_header('Subject', reply_to)
        id = get_header('Message-ID', reply_to)
        message['In-Reply-To'] = id
        references = get_header('References', reply_to)
        if not references:
            references = get_header('In-Reply-To')
        if references:
            message['References'] = references + " " + id
        mail['threadId'] = get_thread_id(reply_to)

    message['To'] = to
    message['Subject'] = subject
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    mail['raw'] = encoded

    return gmail.users().messages().send(userId='me', body=mail).execute()



#dev helper method
def get_most_recent(n=0):
    """Pretty prints and returns most recent email by integer. 0 is most recent."""
    res = gmail.users().messages().list(userId='me', maxResults=n+1).execute()
    messages = res.get('messages')
    if messages:
        id = messages[n]['id']
        print(id)
        mail = gmail.users().messages().get(userId='me', id=id).execute()
        pretty = json.dumps(mail, indent=4)
        print(pretty)
        return mail

if __name__ == '__main__':
    # res, messages = getEmailsFromHistory(2581)
    # print(json.dumps(res, indent=4))
    # for m in messages:
    #     print(m)
    mail = get_most_recent(0)
    body = 'this is a message'
    # print(send_mail(body, reply_to=mail))


#deprecated
def getAllMails():
    # Prints plaintext content of all mails
    # If we return a list of more than 100, we might want to up the maxResults param. If more than 500, we need list_next().
    mails_response = gmail.users().messages().list(userId='me').execute()
    mails = mails_response['messages']
    
    for m in mails:
        actual_mail = gmail.users().messages().get(userId='me', id=m['id']).execute()
        message = getPlainText(actual_mail)
        print(message)
