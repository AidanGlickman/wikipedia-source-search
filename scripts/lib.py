from enum import IntEnum
from typing import List
from datetime import datetime
import xml.etree.ElementTree


class Reliability(IntEnum):
    '''
    The notability of a source. 
    For more info see https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources#Legend
    '''
    STELLAR = -1
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

            if(self.reliability <= Reliability.STELLAR):
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', 'stellar')
                element.append(label)

            if(self.reliability <= Reliability.GENERALLY_RELIABLE):
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', 'generally_reliable')
                element.append(label)
            
            if(self.reliability <= Reliability.NO_CONSENSUS):
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', 'marginally_reliable')
                element.append(label)

                label = xml.etree.ElementTree.Element('Label')
                label.set('name', '_include_')
                element.append(label)
            
            else:
                label = xml.etree.ElementTree.Element('Label')
                label.set('name', '_exclude_')
                element.append(label)

            
            comment = xml.etree.ElementTree.Element('Comment')
            comment.text = str(self)

            element.append(comment)

            elements.append(element)
        return elements

def write_annotations_file(filename: str, *sources: List[Source]):
    '''
    Write the sources to an xml file for use in a Google Programmable Search Engine annotations description file.
    If a source url appears multiple times, the first time it appears will be used.
    For this reason, try to order source lists from most reliable to least reliable.
    '''
    seen_url = set()
    root = xml.etree.ElementTree.Element('Annotations')
    for sourcelist in sources:
        for source in sourcelist:
            xml_vals = source.write_xml()
            for xml_val in xml_vals:
                if xml_val.get('about') in seen_url:
                    continue
                root.append(xml_val)
                seen_url.add(xml_val.get('about'))
    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write(filename, encoding='UTF-8', xml_declaration=True)
