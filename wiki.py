import requests, re, urllib
from bs4 import BeautifulSoup

BASE_EN_URI = 'http://en.wikipedia.org/wiki/'
BASE_DE_URI = 'http://de.wikipedia.org/wiki/'
MAX_STRING_LENGTH = 120

# translation_type = 'ende' or 'deen'
def soup_from_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)

def en_url(query):
    return '%s%s' % (BASE_EN_URI, urllib.quote(query))

def de_url(query):
    return '%s%s' % (BASE_DE_URI, urllib.quote(query))

def wiki(query, english=False):
    if english == False:
        url = de_url(query)
    else:
        url = en_url(query)
    return get_wiki_from_url(url)

def get_wiki_from_url(url):
    soup = soup_from_url(url)
    if soup.select(".noarticletext") != []:
        return 'No entry found [%s]' % url
    sub_soup = soup.find(id="mw-content-text")
    [s.extract() for s in sub_soup('table')]
    [s.extract() for s in sub_soup('div')]
    text = sub_soup.text
    # removes IPA stuff
    text = re.sub('\s*\(.*\[.*\].*?\)', '', text)
    #text = re.sub('\s*\(\/.*\/.*\)', '', text)
    #text = re.sub('\s*\(\s*\[.*\].*\)', '', text)
    # removes notations
    text = re.sub('\[\d*\]', '', text)
    # removes newlines
    text = re.sub('\\n[\s*\\n]+', '\n', text)
    text = re.sub('^\s*\\n\s*', '', text)
    text = re.sub('\\n', ' >> ', text)
    # includes link to wiki article
    if len(text) >= 280:
        next_space_index = text.find(' ', 280)
        if next_space_index != -1:
            text = text[:next_space_index] 
    text = '%s ... [%s]' % (text, url)
    return text.encode('UTF-8')

#a s.find(id='h2').findAll('td', {'class':'r'})
#for i in a:
#    print i.text
