Craigslist Scraper
==================
Scrapes Craigslist for computer gigs (cpg).

Can be adjusted to scrape for other ads by passing a second parameter to the appropriate functions.

Works
-----
- Scrapes first page of jobs given a craigslist region (sfbay, philadelphia, slo, etc.)
- Scrapes the useful information from a particular job
- Stores the scrapted data to a sqlite db
- Can query for words in the texts of the scraped ads

In Progress
-----------
- Classify posting with relevant keywords (tf-idf algorithm)
- Track replied-to postings

Not Yet Implemented
-------------------
- Filter scrapes or db query by relevant keywords (not any words in text)
- Clean workflow for fetching, searching, and marking as replied-to


