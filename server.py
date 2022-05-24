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
            for msg in messages:
                subject, body, mail = msg
                # if 'SENT' in mail['labelIds']:
                #     return ("We sent this message", 200)
                if not gmail.isSpam(body):
                    try:
                        writeToFile('\n' +'New invitation incoming')
                        writeToFile('Predicting event type ...')
                        writeToFile('Email text: '+body)
                        label = classify(body)
                        writeToFile('Event labeled as: ' + label)
                        writeToFile('Predicting start and end for event ...')
                        times = extract_datetime(body)
                        #print("label:", label, "times:", times)
                        print(times)
                        if len(times) == 0: 
                            print("No datetime found.")
                            writeToFile("No datetime found.")
                            raise Exception('No datetime found.')
                        else:
                            writeToFile('Event start predicted to: '+ times[0])
                            writeToFile('Event end predicted to: '+ times[1])
                            names = extract_names(body)
                            description = body
                            if names:
                                description = "Persons: " + names + ". Text: " + body
                            network_response = {
                                'title': subject,
                                'description': description,
                                'tag': label,  # social/business
                                'timeMin': times[0],
                                'timeMax': times[1]
                            }
                            #print("network_response: ", network_response)
                            writeToFile('Checking calender for availability ...')
                            success = events.main(network_response, mail)
                            if success:
                                print("SUCCESS: ",subject) 
                                writeToFile(label+body + " - event created: " + str(success))
                            else:
                                writeToFile('Calender is occupied, event not created')
                                print("FAIL: ",subject)
                            return 'success', 200
                    except Exception as e:
                        print('Insufficient data to build event. ', e)
                        writeToFile('Insufficient data to build event. '+body)
                        return 'Insufficient data to build event.',200
                else:
                    print('Message was spam')
                    return 'Message was spam',200

        else:
            return'no msg',200
    else:
        print(request)
        writeToFile(abort(400))
        return 'megaFail',200
        

@app.route('/')
def catch_all():
    print(request)
    with open(filePath, 'r') as f: 
	    return render_template('console.html', text=f.read()) 

@app.route('/newEvent',methods=['POST'])
def newEvent():
    print('New event incoming')
    id = request.headers.get('X-Goog-Resource-ID')
    if request.method == 'POST': 
        try:
            events.newEvent(id)
            writeToFile('eventcreated')
            return 'success', 200
        except Exception as e:
            #print('Insufficient data to build event. ', e)
            #writeToFile('Insufficient data to build event. ')
            return 'ERROR',500
        

@app.route('/clear')
def clearLog():
    with open(filePath, "w") as f:
        f.write('')
        f.close()
    return 'Log cleared'


def writeToFile(printText):
    with open(filePath, "a") as file:
        currenttime = datetime.datetime.now()
        file.write(str(currenttime)+":"+printText + '\n')


if __name__ == '__main__':
    getCreds()
    watch = gmail.createWatch()
    #events.createWatch()
    most_recent_history_id = watch['historyId']
    app.run(host='0.0.0.0', port=8000)