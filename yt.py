import requests

BASE_URI = 'https://gdata.youtube.com/feeds/api/videos/'

def soup_from_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)

def get_url(id):
    return "%s%s?alt=json" % (BASE_URI, id)

def yt(id):
    get_info(get_url(id))

def get_info(url):
    soup = soup_from_url(url)