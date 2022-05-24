from datetime import datetime, timedelta, timezone

import parsedatetime as pdt
import regex as re
from nltk.tokenize import word_tokenize

relative_time = ['today', 'tomorrow', 'yesterday']
exact_days = ['monday', 'tuesday', 'wednesday',
              'thursday', 'friday', 'saturday', 'sunday']
exact_days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = {
    'Jan': 'January',
    'Feb': 'February',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December',
}

all_signifiers = relative_time + exact_days + exact_days_short


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


def extract_str_dates(text):
    def get_pattern(m):
        return "("+pattern_day+" "+m+")|("+m+" "+pattern_day+")|("+pattern_day_old+m+")"
    pattern_day = "([0-3]?[0-9])(st|th|.)?"
    pattern_day_old = "([0-3]?[0-9])(st|th|.) of "
    dates = {}
    for m in months:
        pattern_date = get_pattern(months[m])
        pattern_date_short = get_pattern(m)
        matches = re.findall(pattern_date, text, re.IGNORECASE)
        if len(matches) == 0:
            matches = matches = re.findall(
                pattern_date_short, text, re.IGNORECASE)
        # remove empty cells in tuple and return 1st item
        filtered_match = [(tuple(x for x in _ if x))[0] for _ in matches]
        if filtered_match:
            d = str(filtered_match[0])
            #print("d", d)
            pos = sum(re.search("".join(d), text).span())/2
            d = d.replace(" of ", " ")
            dates[d] = pos
    return dates


def extract_dates(text):
    def process_dates(txt, dates):
        def us_format(date):
            d = date.split("/")
            if len(d) == 3:
                return d[1] + "/" + d[0] + "/" + d[2]
            else:
                return d[1] + "/" + d[0]
        dates_processed = {}
        for d in dates:
            pos = sum(re.search("".join(d), txt).span())/2
            date_normalised = "".join(d).replace("[^\\d]", "/")
            date_us = us_format(date_normalised)
            dates_processed[date_us] = pos
        return dates_processed
    dates = {}
    pattern_day_month = "([0-3]?[0-9])(/)([0-1])?([0-9])"
    pattern_year = "(/)([1-2][0-9])?([0-9][0-9])"
    matches = re.findall(pattern_day_month + pattern_year, text)
    if len(matches) == 0:
        matches = re.findall(pattern_day_month, text)
    if len(matches) != 0:
        dates = process_dates(text, matches)
    return dates


def pair_by_proximity(key_items, items):
    def get_nearest_item(i, i_pos, near_i, near_i_pos, key_i_pos):
        if abs(i_pos-key_i_pos) < abs(near_i_pos-key_i_pos):
            return (i, i_pos)
        else:
            return (near_i, near_i_pos)
    item_key_item_pairs = []
    for ki in key_items:
        nearest_item = ""
        nearest_item_pos = 99999
        for item in items:
            item_pos = items[item]
            nearest_item, nearest_item_pos = get_nearest_item(
                item,
                item_pos,
                nearest_item,
                nearest_item_pos,
                key_items[ki])
        if (nearest_item != "" and nearest_item_pos != 99999):
            item_key_item_pairs.append([ki, nearest_item])
    return item_key_item_pairs


def parse_sets(sets):
    cal = pdt.Calendar()
    dts = []
    for set in sets:
        dt_string = set[1] + ' at ' + set[0]
        #print("dt_string", dt_string)
        time_struct, parse_status = cal.parse(dt_string)
        if parse_status:
            dt = datetime(
                *time_struct[:6], tzinfo=timezone(timedelta(hours=+2))).isoformat()
            #print("dt", dt)
            # pytz.timezone('Europe/Copenhagen') gives +00:50 for some reason
            dts.append(dt)
    return dts


def parse_items(items, pairs):
    def is_unique(item, pairs):
        for pair in pairs:
            time, date = pair
            if item == time or item == date:
                return False
        return True
    cal = pdt.Calendar()
    dts = []
    for i in items:
        if is_unique(i, pairs):
            time_struct, parse_status = cal.parse(i)
            if parse_status:
                dt = datetime(
                    *time_struct[:3], tzinfo=timezone(timedelta(hours=+2))).isoformat()
                #print("dt", dt)
                date, time = dt.split("T")
                #print("date", date, "time", time)
                time_split = list(time)
                time_split[1] = str(9)
                time_nine = "".join(time_split)
                #print("join", date + "T" + time_nine)
                dt = date + time_nine
                dts.append(dt)
    return dts


def extract_datetime(text):
    def auto_fill_endtime(dts):
        if len(dts) == 1: 
            date, time = dts[0].split("T")
            end = list(time)
            if len(time) == 14:
                new_time = str(min(23, int(time[0]+time[1])+2))
                a, b = list(new_time)
                end[0] = a
                end[1] = b
            else:
                new_time = str(int(time[0])+2)
                if len(new_time) == 1:
                    end[0] = new_time
                else:
                    a, b = list(new_time)
                    end[0] = a
                    end[1] = b
            dts.append("".join(end))
        return dts
    signifiers = extract_signifiers(text)
    num_dates = extract_dates(text)
    str_dates = extract_str_dates(text)
    #print("s", signifiers)
    dates = {**num_dates, **str_dates, **signifiers}
    #print("d", dates)
    times = extract_time(text)
    # print(times)
    pairs = pair_by_proximity(times, dates)
    dts = []
    if pairs:
        parsed = parse_sets(pairs)
        if parsed:
            dts += parsed
    if dates:
        parsed = parse_items(dates, pairs)
        # print("p",parsed)
        if parsed:
            dts += parsed

    dts = auto_fill_endtime(dts)
    print(dts)
    return dts

if __name__ == '__main__':
    text = "There is a party at the 11th of july 10:00. It ends at 16:00. Also party at 22/01/23 at 14:00 and at aug 13 00:00"
    text = "If you would come by my office after work, let's say Tuesday at 17:00, we can discuss that business matter you brought up earlier. We should be done by 19:00"
    # text = "Hej Johan."
    datetime = extract_datetime(text)
    print(text)
    print(datetime)
