import requests, json, re

BASE_URI = 'https://gdata.youtube.com/feeds/api/videos/'

def trim(text, max_length):
    if len(text) > max_length:
        next_space_index = text.find(' ', max_length + 1)
        if next_space_index != -1:
            text = text[:next_space_index] + '...'
    return text

def seconds_to_hms(total_seconds):
    total_seconds = int(total_seconds)
    hours = total_seconds / 3600
    minutes = (total_seconds % 3600) / 60
    seconds = total_seconds % 60
    if hours > 0:
        return "%dh:%02dm:%02ds" % (hours, minutes, seconds)
    else:
        return "%dm:%02ds" % (minutes, seconds)

def dict_from_url(url):
    r = requests.get(url)
    try:
        json_dict = json.loads(r.text)
        return json_dict
    except ValueError:
        return None

def get_url_for_id(id):
    return "%s%s?alt=json" % (BASE_URI, id)

def yt(id):
    return get_info(id)

def get_info(id):
    json_dict = dict_from_url(get_url_for_id(id))
    if json_dict != None:
        title = json_dict['entry']['title']['$t']
        desc = trim(json_dict['entry']['media$group']['media$description']['$t'], 180)
        rating = "%.1f" % json_dict['entry']['gd$rating']['average']
        total_rates = json_dict['entry']['gd$rating']['numRaters']
        views = json_dict['entry']['yt$statistics']['viewCount']
        dur = seconds_to_hms(json_dict['entry']['media$group']['yt$duration']['seconds'])
        short_link = "http://youtu.be/%s" % id
        return_string = '[%s] %s || "%s" || %s || avg. %s of %s votes || %s views' % (short_link, title, desc, dur, rating, total_rates, views)
        # removes new lines
        return_string = re.sub('\\n', '', return_string)
        return return_string.encode('UTF-8')
    else:
        return None

