import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import parsedatetime as pdt
from datetime import datetime
import regex as re

relative_time = ['today', 'tomorrow', 'yesterday']
exact_days = ['monday', 'tuesday', 'wednesday',
              'thursday', 'friday', 'saturday', 'sunday']
exact_days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
all_signifiers = relative_time + exact_days + \
    exact_days_short + months + months_short

def extract_signifiers(text):
    signifiers = {}
    tokens = word_tokenize(text)
    signifier_tokens = [
        t for t in tokens for s in all_signifiers if t.lower() == s.lower()]
    if signifier_tokens:
        for s in signifier_tokens:
            pos = sum(re.search(s, text).span())/2
            signifiers[s] = pos
    return signifiers

def extract_time(text):
    times = {}
    matches = re.findall("([0-2][0-9]|[0-9])(:|\.)?([0-6][0-9])", text)
    if matches:
        for match in matches:
            pos = sum(re.search("".join(match), text).span())/2
            time = str(match[0]) + ":" + str(match[2])
            times[time] = pos
    return times

def extract_dates(text):
    def process_dates(txt, dates):
        dates_processed = {}
        for d in dates:
            pos = sum(re.search("".join(d), txt).span())/2
            date_processed = "".join(d).replace("[^\\d]", "/")
            dates_processed[date_processed] = pos
        return dates_processed
    dates = {}
    pattern_day_month = "([0-3]?[1-9])(/|\.)([0-1])?([0-9])"
    pattern_year = "(/|\.)([1-2][0-9])?([0-9][0-9])"
    matches = re.findall(pattern_day_month + pattern_year, text)
    if len(matches) == 0:
        matches = re.findall(pattern_day_month, text)
    if len(matches) != 0:
        dates = process_dates(text, matches)
    return dates

def match_time_signifiers(times, signifiers):
    def get_closest_time(a, a_pos, b, b_pos, s_pos):
        if abs(a_pos-s_pos) < abs(b_pos-s_pos):
            return (a, a_pos)
        else:
            return (b, b_pos)

    time_sets = []
    for s in signifiers:
        closest_time = "99:99"
        closest_time_pos = 999
        for t in times:
            t_pos = times[t]
            closest_time, closest_time_pos = get_closest_time(
                t, t_pos, closest_time, closest_time_pos, signifiers[s])
        time_sets.append([s, closest_time])
    return time_sets


def parse_sets(sets, as_string):
    cal = pdt.Calendar()
    dts = []
    for set in sets:
        time_struct, parse_status = cal.parse(set[0] + ' ' + set[1])
        if parse_status:
            dt = datetime(*time_struct[:6])
            if as_string:
                dts.append(str(dt))
            else:
                dts.append(dt)
    return dts


def parse_items(items, as_string):
    cal = pdt.Calendar()
    dts = []
    for i in items:
        time_struct, parse_status = cal.parse(i)
        if parse_status:
            dt = datetime(*time_struct[:6])
            if as_string:
                dts.append(str(dt))
            else:
                dts.append(dt)
    return dts

def process(text):
    print(text)
    cal = pdt.Calendar()
    signifiers = extract_signifiers(text)
    times = extract_time(text)
    time_sets = match_time_signifiers(times, signifiers)
    dates = extract_dates(text)
    dt_sets = parse_sets(time_sets, True)
    dt_items = parse_items(signifiers, True)
    print(dates)
    #print("S:", signifiers)
    #print("T:", times)
    #print("SETS:", time_sets)
    #print("DT SETS:", dt_sets)
    #print("DT SIGNIFIERS:", dt_items)
    # dt = datetime(*time_struct[:6])
    # print(dt)

# def process(sentence):
#    cal = pdt.Calendar()
#    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
#        if (t1 == 'NN' and t3 == 'CD'):
#            print(w1, w2, w3)
#            time_struct, parse_status = cal.parse(w1 + ' ' + w2 + ' ' + w3)
#            if (parse_status):
#                print("Parse succesful.")
#                return datetime(*time_struct[:6])
#        if (t1 == 'CD' and t3 == 'NN'):
#            time_struct, parse_status = cal.parse(w1 + w2 + w3)
#            if (parse_status):
#                print("Parse succesful.")
#                return datetime(*time_struct[:6])


def tokenize(text):
    return word_tokenize(text)


def pos_tag(tokens):
    return nltk.pos_tag(tokens)


if __name__ == '__main__':
    text = "Hello Johan. Ignore the number 11:55. We would like to invite you for an interview tomorrow at 14:00. Alternatively, we'd be available monday at 12:00. We would also like to meet 18/10/22 at 9:00 and on 29/09/2022 and on 1/1/99"
    process(text)
