import base64
from flask import Flask,request, abort,render_template 
import sys
import datetime
import json
import gmail
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

app = Flask(__name__)

filePath = 'templates/serverConsole.txt'
most_recent_history_id = None
messages = None
res = None



@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # writeToFile(request.json)
        # decoded = base64.urlsafe_b64decode(request.json['message']['data'].encode()).decode()
        # decoded_dict = json.loads(decoded)
        # history_id = decoded_dict['historyId']
        global most_recent_history_id
        global res
        global messages
        res, messages = gmail.getEmailsFromHistory(most_recent_history_id)
        most_recent_history_id = res['historyId']
        writeToFile(messages)
        
        
        return 'success', 200

    else:
        print(request)
        writeToFile(abort(400))
        

@app.route('/')
def catch_all():
    with open(filePath, 'r') as f: 
	    return render_template('console.html', text=f.read()) 


@app.route('/clear')
def clearLog():
    with open(filePath, "w") as f:
        f.write('')
        f.close()
    return 'Log cleared'


def writeToFile(printText):
    sys.stdout = open(filePath, "a")
    currenttime = datetime.datetime.now()
    print(currenttime, printText)
    sys.stdout.close()


def getCreds():
    

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://mail.google.com/']

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


if __name__ == '__main__':
    getCreds()
    watch = gmail.createWatch()
    most_recent_history_id = watch['historyId']
    app.run(host='0.0.0.0', port=8000)       