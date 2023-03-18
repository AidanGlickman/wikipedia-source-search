'''
Wikipedia Perennial Source Scraper
'''

import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from urllib import parse as urlparse
from lib import Reliability, Source

BASE_URL = 'https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources'

TABLE_CLASS = 'perennial-sources'

def get_table() -> BeautifulSoup:
    '''Get the table of perennial sources from Wikipedia'''
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': TABLE_CLASS})
    return table


def process_source(source: BeautifulSoup) -> Source:
    '''
    Process a source from the table
    @param source: The source to process
    '''
    cells = source.find_all('td')

    name = cells[0].text

    try:
        article = cells[0].find('a').get('href')
    except AttributeError:
        article = None
    
    reliability = int(cells[1]['data-sort-value'])
    reliability = Reliability(reliability if reliability < 10 else 10)

    last = cells[3]['data-sort-value']
    last = datetime.strptime(last, '%Y')

    summary = cells[4].text

    links = []
    for link in cells[5].find_all('a'):
        url = urlparse.urlparse(link.get('href'))
        if 'wikipedia.org' in url.netloc:
            target = urlparse.parse_qs(url.query)['target'][0]
            if 'https' in target:
                continue
            links.append(target + "/*")

    return Source(name, reliability, last, summary, links)


def process_sources(table) -> List[Source]:
    '''
    Process all the sources in a table
    @param table: the table of sources
    @return sources: a list of source objects
    '''
    sources = []
    for row in table.find_all('tr'):
        if(row.find('th')):
            continue
        source = process_source(row)
        sources.append(source)
    return sources
