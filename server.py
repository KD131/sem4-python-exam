from flask import Flask,request, abort,render_template 
import sys
import datetime
import gmail
from credentials import getCreds
from neural_network.neuralClass import classify
app = Flask(__name__)

filePath = 'templates/serverConsole.txt'
most_recent_history_id = None




@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # writeToFile(request.json)
        # decoded = base64.urlsafe_b64decode(request.json['message']['data'].encode()).decode()
        # decoded_dict = json.loads(decoded)
        # history_id = decoded_dict['historyId']
        global most_recent_history_id
        res, messages = gmail.getEmailsFromHistory(most_recent_history_id)
        most_recent_history_id = res['historyId']
        if(messages):
            for msg in messages:
                try:
                    label = classify(msg)
                    print(label)
                    writeToFile(label+msg)
                    return 'success', 200
                except Exception as e:
                    print(e)
                    writeToFile('failed to predict'+msg)
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
    sys.stdout = open(filePath, "a")
    currenttime = datetime.datetime.now()
    print(currenttime, printText)
    sys.stdout.close()


if __name__ == '__main__':
    getCreds()
    watch = gmail.createWatch()
    most_recent_history_id = watch['historyId']
    app.run(host='0.0.0.0', port=8000)       