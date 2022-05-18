import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import parsedatetime as pdt
from datetime import datetime
import regex as re

relative_time = ['today', 'tomorrow', 'yesterday', 'week', 'month', 'year', 'fortnight']
exact_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
exact_days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
triggers = relative_time + exact_days + exact_days_short + months + months_short

def extract_time(text):
    sentences = sent_tokenize(text)
    print(text)
    cal = pdt.Calendar()
    #for s in sentences:
    time_words_log = {}
    time_log = {}
    time_sets = []
    words = word_tokenize(text)
    time_words = [w for w in words for t in triggers if w.lower() == t]
    if time_words:
        for w in time_words:
            pos = sum(re.search(w, text).span())/2
            time_words_log[w] = pos
    
    reg = re.findall("([0-2][0-9]|[0-9])(:|\.|\b)?([0-6][0-9])", text)
    if reg:
        for match in reg:
            pos = sum(re.search("".join(match), text).span())/2
            time = str(match[0]) + ":" + str(match[2])
            time_log[time] = pos
    for w in time_words_log:
        closest_time = ""
        closest_time_pos = 999
        for t in time_log:
            if time_log[t] - time_words_log[w] < closest_time_pos:
                closest_time_pos = time_log[t] - time_words_log[w]
                closest_time = t
        time_sets.append([w, closest_time])
    print(time_sets)
    #dt = datetime(*time_struct[:6])
    #print(dt)

def process(sentence):
    cal = pdt.Calendar()
    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
        if (t1 == 'NN' and t3 == 'CD'):
            print(w1, w2, w3)
            time_struct, parse_status = cal.parse(w1 + ' ' + w2 + ' ' + w3)
            if (parse_status):
                print("Parse succesful.")
                return datetime(*time_struct[:6])
        if (t1 == 'CD' and t3 == 'NN'):
            time_struct, parse_status = cal.parse(w1 + w2 + w3)
            if (parse_status):
                print("Parse succesful.")
                return datetime(*time_struct[:6])
            
def tokenize(text):
    return word_tokenize(text)

def pos_tag(tokens):
    return nltk.pos_tag(tokens)

if __name__ == '__main__':
    text = "Hello Johan. Ignore the number 11:55. We would like to invite you for an interview tomorrow at 14:00. Alternatively, we'd be available 16/06 at 12:00"
    extract_time(text)
    #text = tokenize(text)
    #text = pos_tag(text)
    #print(text)
    #dt = process(text)
    #print(dt)
    #cal = pdt.Calendar()
    #time_struct, parse_status = cal.parse("faz")
    #dt = datetime(*time_struct[:6])
    #print(dt, parse_status)
