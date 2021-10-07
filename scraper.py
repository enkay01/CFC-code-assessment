from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from contextlib import closing
import json


url = 'http://www.cfcunderwriting.com'

def simple_get(url):
    try:
        with closing( get(url, stream=True) ) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print("Error during requests to {0} : {1}".format(url, str(e)))
        return None

def is_good_response(resp):
    "Returns true if respons contains HTML"
    
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def write_to_json(data):
    with open('external resources.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)


raw_html = simple_get(url)
html = BeautifulSoup(raw_html, 'html.parser')
head = html.head
links = head.find_all('link')
external_res = []
for x in links:
    if x.name == 'link':
        if "cfcunderwriting.com" not in x.get('href'):
            external_res.append(x.get('href'))

write_to_json(external_res)