from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from contextlib import closing


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

raw_html = simple_get(url)
html = BeautifulSoup(raw_html, 'html.parser')
head = html.head
links = head.find_all('link')
external_res = []
for x in links:
    if x.name == 'link':
        if "cfcunderwriting.com" not in x.get('href'):
            external_res.append(x)
print(external_res)