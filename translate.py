# coding=UTF-8
import requests, urllib
from bs4 import BeautifulSoup

BASE_URI = 'http://dict.tu-chemnitz.de/dings.cgi'
DEEN_STR = 'de-en'
ENDE_STR = 'en-de'

NO_RESULTS = {
    'de-en': 'No results found.',
    'en-de': u'Keine Einträge gefunden.'
}

NUM_TRANSLATIONS = 3

# translation_type = 'ende' or 'deen'
def soup_from_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)

def translate_url(translation_type, query):
    return '%s?lang=en&service=%s&query=%s' % (BASE_URI, translation_type, urllib.quote(query))

def ende(query):
    url = translate_url(ENDE_STR, query)
    return get_translations(ENDE_STR, url)

def deen(query):
    print 'deen'
    url = translate_url(DEEN_STR, query)
    return get_translations(DEEN_STR, url)

def get_translations(translation_type, url):
    print 'get_translations'
    soup = soup_from_url(url)
    translations = []
    for i in range(1, NUM_TRANSLATIONS + 1):
        sub_soup = soup.find(id='h%s' % i)
        if sub_soup == None:
            break
        else:
            lst = sub_soup.findAll('td', {'class':'r'})
            translation_string = '%s = %s' % (lst[0].text.strip(), lst[1].text.strip())
            translations.append(translation_string)
    if len(translations) > 0:
        translations = " || ".join(translations)
        translations = "%s [%s]" % (translations, url)
    else:
        translations = "%s [%s]" % (NO_RESULTS[translation_type], url)
    return translations.encode('UTF-8')

#a s.find(id='h2').findAll('td', {'class':'r'})
#for i in a:
#  	 print i.text
