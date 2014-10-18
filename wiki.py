import requests, re
from bs4 import BeautifulSoup

BASE_EN_URI = 'http://en.wikipedia.org/wiki/'
BASE_DE_URI = 'http://de.wikipedia.org/wiki/'
MAX_STRING_LENGTH = 120

# translation_type = 'ende' or 'deen'
def soup_from_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)

def en_url(query):
    return '%s%s' % (BASE_EN_URI, query)

def de_url(query):
    return '%s%s' % (BASE_DE_URI, query)

def wiki(query, english=False):
    if english == False:
        url = de_url(query)
    else:
        url = en_url(query)
    return get_wiki_from_url(url)

def get_wiki_from_url(url):
    soup = soup_from_url(url)
    sub_soup = soup.find(id="mw-content-text")
    text = sub_soup.p.text
    if len(text) >= 280:
        next_space_index = text.find(' ', 280)
        if next_space_index != -1:
            text = text[:next_space_index]
    # removes IPA stuff
    text = re.sub('\s*\(\/.*\/.*\)', '', text)
    text = re.sub('\s*\(\s*\[.*\].*\)', '', text)
    # removes notations
    text = re.sub('\[\d*\]', '', text)
    # removes newlines
    text = re.sub('\\n', '', text)
    # includes link to wiki article
    text = '%s ... [%s]' % (text, url)
    return text.encode('UTF-8')

#a s.find(id='h2').findAll('td', {'class':'r'})
#for i in a:
#    print i.text
