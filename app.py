import requests, bs4

BASE_URI = 'http://dict.tu-chemnitz.de/dings.cgi?'
DEEN_STR = 'de-en'
ENDE_STR = 'en-de'

# translation_type = 'ende' or 'deen'
def beo_request_text(translation_type, query):
	r = requests.get('%s?lang=en&service=%s&query=%s' % (BASE_URI, translation_type, query))
	return r.text

def ende_query_text(query):
	return beo_request_text(ENDE_STR, query)

def deen_query_text(query):
	return beo_request_text(DEEN_STR, query)

