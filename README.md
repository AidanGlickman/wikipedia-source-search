# Wikipedia Perennial Sources Search

This project uses [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/) to provide a quick and easy way to find sources that establish notability for Wikipedia articles. It pulls from [Wikipedia:Reliable_Sources/Perennial_Sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources) list. Note that this is _not_ a comprehensive list, and is only meant to be a starting point for finding sources.

## How to use

This project implements two different search engines:

### PS_Generally-Reliable

This search engine indexes pages listed as generally reliable on the [Wikipedia:Reliable_Sources/Perennial_Sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources) list. It is the strictest subset on this list, and has a very good chance of establishing notability for an article.

### PS_Marginally-Reliable

This search engine indexes pages listed as generally reliable, as well as those that are marginally reliable (no consensus) on the [Wikipedia:Reliable_Sources/Perennial_Sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources) list. These sources are less strict than those in [PS_Generally-Reliable](#ps_generally-reliable), but still have a good chance of establishing notability for an article.
