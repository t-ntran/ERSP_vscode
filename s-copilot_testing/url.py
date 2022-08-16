from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

def main(url):
    req = Request(url, 
    headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    with open('urls.txt', 'w') as f:
        for link in links:
            f.write(link.get('href') + '\n')
    f.close()




main('https://www.google.com')