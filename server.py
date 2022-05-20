import datetime
import random as rnd
import sys

from flask import Flask, abort, render_template, request

import events
import gmail
from credentials import getCreds
from neural_network.neuralClass import classify
from datetime_extractor import extract_datetime
from name_extractor import extract_names

app = Flask(__name__)

filePath = 'templates/serverConsole.txt'
most_recent_history_id = None


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        global most_recent_history_id
        res, messages = gmail.getEmailsFromHistory(most_recent_history_id)
        most_recent_history_id = res['historyId']
        if(messages):
            if not gmail.isSpam(body):
                for msg in messages:
                    subject, body = msg
                    try:
                        label = classify(body)
                        times = extract_datetime(body)
                        if len(times) == 0: raise("No datetime found.")
                        names = extract_names(body)
                        network_response = {
                            'title': subject,
                            'description': body,
                            'tag': label,  # social/business
                            'timeMin': times[0],
                            'timeMax': times[1]
                        }
                        print("network_response: ",network_response)
                        success = events.main(network_response)
                        writeToFile(label+body + " - event created: " + str(success))
                        return 'success', 200
                    except Exception as e:
                        print(e)
                        writeToFile('Insufficient data to build event'+body)
                        return 'Insufficient data to build event',500
        else:
            return'no msg',200
    else:
        print(request)
        writeToFile(abort(400))
        return 'megaFail',500
        

@app.route('/')
def catch_all():
    print(request)
    with open(filePath, 'r') as f: 
	    return render_template('console.html', text=f.read()) 

@app.route('/newEvent')
def newEvent():
    if request.method == 'POST':
        print(request['id'])
        events.newEvent(request['id'])


@app.route('/clear')
def clearLog():
    with open(filePath, "w") as f:
        f.write('')
        f.close()
    return 'Log cleared'


def writeToFile(printText):
    with open(filePath, "a") as file:
        currenttime = datetime.datetime.now()
        file.write(str(currenttime)+":"+printText)


if __name__ == '__main__':
    getCreds()
    watch = gmail.createWatch()
    events.createWatch()
    most_recent_history_id = watch['historyId']
    app.run(host='0.0.0.0', port=8000)