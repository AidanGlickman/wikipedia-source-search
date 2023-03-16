'''
Wikipedia Perenial Source Scraper
'''

import requests
from bs4 import BeautifulSoup
from enum import Enum
from typing import List
from datetime import datetime
from urllib import parse as urlparse

BASE_URL = 'https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources'

TABLE_CLASS = 'perennial-sources'


class Reliability(Enum):
    '''
    The notability of a source. 
    For more info see https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources#Legend
    '''
    GENERALLY_RELIABLE = 0
    NO_CONSENSUS = 1
    GENERALLY_UNRELIABLE = 2
    DEPRECATED = 3
    BLACKLISTED = 10

    def __str__(self):
        return self.name
    
class Source:
    def __init__(self, name: str, reliability: str, last: datetime, summary: str, links: List[str]):
        self.name = name
        self.reliability = reliability
        self.last = last
        self.summary = summary
        self.links = links
    
    def __str__(self):
        return f'{self.name} ({self.reliability}) - {self.last}\n {self.summary}\n {self.links}'
    
    def __repr__(self):
        return self.__str__()


def get_table():
    '''Get the table of perennial sources from Wikipedia'''
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': TABLE_CLASS})
    return table


def process_source(source):
    '''
    Process a source from the table
    @param source: The source to process
    '''
    cells = source.find_all('td')
    # for i, cell in enumerate(cells):
    #     print(f'Cell {i}:\n')
    #     print(cell.prettify())
    #     print('\n-----------------\n')
    #     input()
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
            links.append(target)

    # print(name, reliability, links)
    return Source(name, reliability, last, summary, links)


def process_sources(table):
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


if __name__ == '__main__':
    table = get_table()
    sources = process_sources(table)
    print(sources)
