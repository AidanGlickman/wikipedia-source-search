import json
from lib import Source, Reliability
from datetime import datetime
def process_news(path="CiteUnseen/data/categorized-domains.json"):
    '''
    Scrapes the citeunseen submodule for sources considered as "news". 
    These are categorized as generally reliable by default.
    '''
    with open(path, "r") as f:
        data = json.load(f)
    sources = []
    for source in data["news"]:
        sources.append(Source(source, Reliability.GENERALLY_RELIABLE, datetime.now(), "News source specified in CiteUnseen", ['*.'+source+'/*']))
    return sources
