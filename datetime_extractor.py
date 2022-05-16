import nltk
from nltk.tokenize import word_tokenize
import parsedatetime as pdt
from datetime import datetime


def process(sentence):
    # [_three-word]
    cal = pdt.Calendar()
    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
        if (t1 == 'NN' and t3 == 'CD'):
            print(w1, w2, w3)  # [_print-words]
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
    text = "Hello Johan. We would like to invite you for an interview tomorrow at 12:00. Alternatively, we'd be available 16/06 at 12:00"
    text = tokenize(text)
    text = pos_tag(text)
    dt = process(text)
    print(dt)
    #cal = pdt.Calendar()
    #time_struct, parse_status = cal.parse("faz")
    #dt = datetime(*time_struct[:6])
    #print(dt, parse_status)
