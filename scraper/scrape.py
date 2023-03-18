'''
Wikipedia Perennial Source Scraper
'''

import requests
from bs4 import BeautifulSoup
from enum import IntEnum
from typing import List
from datetime import datetime
from urllib import parse as urlparse
import xml.etree.ElementTree

BASE_URL = 'https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources'

TABLE_CLASS = 'perennial-sources'


class Reliability(IntEnum):
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
        self.name = name.strip()
        self.reliability = reliability
        self.last = last
        self.summary = summary
        self.links = links
    
    def __str__(self):
        return f'{self.name} ({self.reliability}) - {self.last.year}\n {self.summary}'
    
    def __repr__(self):
        return self.__str__()
    
    def write_xml(self) -> List[xml.etree.ElementTree.Element]:
        '''
        Write the source to a list of xml elements for each link.
        These elements are for use in a Google Programmable Search Engine annotations description file.
        '''
        elements = []
        for link in self.links:
            element = xml.etree.ElementTree.Element('Annotation')
            element.set('about', link)
            # time since epoch in microseconds
            # element.set('timestamp', hex(int(datetime.now().timestamp()*1000000)))

            label = xml.etree.ElementTree.Element('Label')
            label.set('name', '_include_')
            element.append(label)

            if(self.reliability <= Reliability.GENERALLY_RELIABLE):
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', 'generally_reliable')
                element.append(label)
            
            if(self.reliability <= Reliability.NO_CONSENSUS):
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', 'marginally_reliable')
                element.append(label)
            
            comment = xml.etree.ElementTree.Element('Comment')
            comment.text = str(self)

            element.append(comment)

            elements.append(element)
        return elements


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

def write_annotations_file(sources: List[Source], filename: str):
    '''
    Write the sources to an xml file for use in a Google Programmable Search Engine annotations description file.
    '''
    root = xml.etree.ElementTree.Element('Annotations')
    for source in sources:
        xml_vals = source.write_xml()
        for xml_val in xml_vals:
            root.append(xml_val)
    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write(filename)


if __name__ == '__main__':
    table = get_table()
    sources = process_sources(table)
    write_annotations_file(sources, 'annotations.xml')
