import datetime
import random as rnd
import sys

from flask import Flask, abort, render_template, request

import events
import gmail
from credentials import getCreds
from neural_network.neuralClass import classify

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
            for msg in messages:
                subject, body = msg
                try:
                    label = classify(body)
                    #print(label)
                    day = rnd.randint(18, 20) 
                    network_response = {
                        'title': subject,
                        'description': body,
                        'tag': label,  # social/business
                        'timeMin': '2022-05-' + day + 'T13:00:00+02:00',
                        'timeMax': '2022-05-' + day + 'T16:30:00+02:00'
                    }
                    success = events.main(network_response)
                    writeToFile(label+body + " - event created: " + success)
                    return 'success', 200
                except Exception as e:
                    print(e)
                    writeToFile('failed to predict'+body)
                    return 'Predition failed',500
        else:
            return'no msg',200
    else:
        print(request)
        writeToFile(abort(400))
        return 'megaFail',500
        

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
    with open(filePath, "a") as file:
        currenttime = datetime.datetime.now()
        file.write(str(currenttime)+":"+printText)


if __name__ == '__main__':
    getCreds()
    watch = gmail.createWatch()
    most_recent_history_id = watch['historyId']
    app.run(host='0.0.0.0', port=8000)       
