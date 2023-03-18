import sources.citeunseen as citeunseen
import sources.scrape as scrape
from lib import *

if __name__ == "__main__":
    perennial_sources = scrape.process_sources(scrape.get_table())
    cite_unseen_news = citeunseen.process_news()
    write_annotations_file('out/annotations.xml', perennial_sources, cite_unseen_news)
