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
            pos = sum(re.search("".join(d), text).span())/2
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
        avail_items = items
        for item in avail_items:
            item_pos = avail_items[item]
            nearest_item, nearest_item_pos = get_nearest_item(
                item,
                item_pos,
                nearest_item,
                nearest_item_pos,
                key_items[ki])
        if (nearest_item != "" and nearest_item_pos != 99999):
            item_key_item_pairs.append([ki, nearest_item])
            del avail_items[item]
    return item_key_item_pairs


def parse_sets(sets):
    cal = pdt.Calendar()
    dts = []
    for set in sets:
        dt_string = set[0] + ' ' + set[1]
        time_struct, parse_status = cal.parse(dt_string)
        if parse_status:
            dt = datetime(
                *time_struct[:6], tzinfo=timezone(timedelta(hours=+2))).isoformat()
            # pytz.timezone('Europe/Copenhagen') gives +00:50 for some reason
            dts.append(dt)
    dts.sort()
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
                    *time_struct[:6], tzinfo=timezone(timedelta(hours=+2))).isoformat()
                dts.append(dt)
    dts.sort()
    return dts


def extract_datetime(text):
    signifiers = extract_signifiers(text)
    dates = extract_dates(text)
    times = extract_time(text)
    str_dates = extract_str_dates(text)
    pairs = pair_by_proximity(times, {**dates, **str_dates, **signifiers})
    dts = []
    print(signifiers)
    if pairs:
        parsed = parse_sets(pairs)
        if parsed:
            dts.append(parsed)
    if dates:
        parsed = parse_items(dates, pairs)
        if parsed:
            dts.append(parsed)
    if str_dates:
        parsed = parse_items(str_dates, pairs)
        if parsed:
            dts.append(parsed)

    if signifiers:
        parsed = parse_items(signifiers, pairs)
        if parsed:
            dts.append(parsed)

    if times:
        parsed = parse_items(times, pairs)
        if parsed:
            dts.append(parsed)

    return dts


if __name__ == '__main__':
    text = "Hello Johan. Ignore the number. We would like to invite you for a crazy party begining today at 10:00 and ending tomorrow"
    #text = "Hej Johan."
    datetime = extract_datetime(text)
    print(text)
    print(datetime)
