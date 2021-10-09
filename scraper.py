from requests import get
from collections import Counter
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from contextlib import closing
import json


url = 'http://www.cfcunderwriting.com'
priv_pol_link = None
HTML_PARSER = 'html5lib'

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
    #Returns true if respons contains HTML
    
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

#Gets head of web page. Finds all links. Returns string list of links
def get_external_resources(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, HTML_PARSER)
    head = html.head
    links = head.find_all('link')
    external_res = []
    for x in links:
        if x.name == 'link' and "cfcunderwriting.com" not in x.get('href'):
            external_res.append(x.get('href'))

    return external_res
#Gets body of web page Finds all links. Returns string list of links
def find_all_links(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, HTML_PARSER)
    body = html.body
    links = body.find_all('a')
    hyperlinks = []
    for l in links:
        if not '#' in l.get('href', []):
            hyperlinks.append(l.get('href', []))
    return hyperlinks
#Takes main element of page. Removes whitespace, punctuation, and numbers. Returns list of words.
def scrape_page_text(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, HTML_PARSER)
    main = html.find('main')
    text = main.text.strip()
    text = ''.join(e for e in text if e.isalnum() or " " in e)
    words = text.split(" ")
     
    return words
#Returns dictionary of words with counts
def count_words(word_list):
    return Counter(word_list)

if __name__ == '__main__':
    external_res = get_external_resources(url)
    write_to_json(external_res, 'external resources.json')
    links = find_all_links(url)
    
    for l in links: 
        if "privacy-policy" in l:
            priv_pol_link = url + l
    main = scrape_page_text(priv_pol_link)   
    counts = count_words(main)
    write_to_json(counts, 'word counts.json')