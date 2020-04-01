Craigslist Scraper
==================
Scrapes Craigslist for ads.

Stores the scraped data in a directory structure in txt format, and in json
format if the `jq` command is present.

Searches one region at a time; available regions are listed in `locations.txt`.

Examples
--------

::

    $ craigslist-gigs sfbay  # computer gigs by default
    $ craigslist-gigs --gig computer-gig --outdir /tmp/gigs --region sfbay
    $ craigslist-gigs --gig creative --region washingtondc

Output example
--------------

::

    craigslist-gigs-output/
    ├── sfbay
    │   ├── 7086886670.json
    │   ├── 7086886670.txt
    │   ├── 7086909144.json
    │   ├── 7086909144.txt
    │   ├── 7087168622.json
    │   ├── 7087168622.txt
    │  ...
    │   ├── 7101838004.json
    │   └── 7101838004.txt
    └── washingtondc
        ├── 7085989259.json
        ├── 7085989259.txt
        ├── 7086514642.json
        ├── 7086514642.txt
       ...
        ├── 7101568324.json
        └── 7101568324.txt

Maintainer
==========

Med Mahmoud <medthehatta@gmail.com>
