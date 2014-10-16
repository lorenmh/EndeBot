import requests
from bs4 import BeautifulSoup

BASE_URI = 'http://dict.tu-chemnitz.de/dings.cgi?'
DEEN_STR = 'de-en'
ENDE_STR = 'en-de'
NUM_TRANSLATIONS = 3

# translation_type = 'ende' or 'deen'
def beo_request_text(translation_type, query):
	r = requests.get('%s?lang=en&service=%s&query=%s' % (BASE_URI, translation_type, query))
	return r.text

def ende_query_text(query):
	return beo_request_text(ENDE_STR, query)

def deen_query_text(query):
	return beo_request_text(DEEN_STR, query)

def ende(query):
	s = BeautifulSoup(ende_query_text(query))
	return get_translations(s)

def deen(query):
	s = BeautifulSoup(deen_query_text(query))
	return get_translations(s)

def get_translations(soup):
	return get_num_translations(NUM_TRANSLATIONS, soup)

def get_num_translations(num, soup):
	translations = []
	for i in range(1, num + 1):
		sub_soup = soup.find(id='h%s' % i)
		if sub_soup == None:
			break
		else:
			lst = sub_soup.findAll('td', {'class':'r'})
			translation_string = '%s = %s' % (lst[0].text.strip(), lst[1].text.strip())
			translations.append(translation_string)
	return translations

#a s.find(id='h2').findAll('td', {'class':'r'})
#for i in a:
#  	 print i.text
