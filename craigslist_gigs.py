import re
import urllib.request
import random
import datetime
import sqlite3
import time
import sys
import argparse
from itertools import count
from bs4 import BeautifulSoup


def get_places(): 
    """Loads the craigslist locations like sfbay, philadelphia, etc."""
    FP = "cl_locations.dat"
    try:
        return open(FP).read().split("\n")
    except IOError:
        print("Unable to open location file at: {}".format(FP))
        return None


def get_soup(url):
    """
    Reads an url with urllib, does some rudimentary error-checking, and returns
    soup
    """
    try:
        ret = urllib.request.urlopen(url)
        if ret.status == 200:
            return BeautifulSoup(ret.read())
    except Exception:
        return None
    

def get_links(place,subcat):
    """
    Reads all the links on the first page of a craigslist location.
    """
    url = "http://{}.craigslist.org".format(place)
    soup = get_soup(url+'/{}/'.format(subcat))
    if soup is not None:
        href_match = re.compile(r'^(?:/[a-z]+)*/'+subcat+'/[0-9]+.html')
        text_match = lambda t: t is not None
        links = soup.find_all(attrs={'href':href_match},text=text_match)
        ret_links = [(url+link.attrs['href'],link.text) for link in links]
        return ret_links


def get_posting(url):
    """
    Fetches the soup for a specific posting and then processes it.  Basically a
    wrapper around get_posting_info.
    """
    soup = get_soup(url)
    if soup is not None:
        return get_posting_info(soup,url)


def get_posting_info(soup,url):
    """
    Given soup for a posting page, extracts the important properties from the
    page and returns a dict.
    """
    try:
        date = soup.find('date').text.strip().split(', ')
        posting_date = datetime.datetime.strptime(date[0],"%Y-%m-%d")
        posting_time = date[1]

        posting_text = soup.find(attrs={'id':'postingbody'}).text.strip()
        posting_title = soup.find(attrs={'class':'postingtitle'}).text.strip()
        posting_email = soup.find(attrs={'href':re.compile(r'mailto.*')})
        if posting_email is not None:
            posting_email = posting_email.text.strip()
        else:
            posting_email = "nobody"
    except Exception:
        posting_text = "(fail)"
        posting_title = "(fail)"
        posting_email = "(fail)"
        posting_date = "(fail)"
        posting_time = "(fail)"

    return {'email':posting_email, 'date':posting_date, 'time':posting_time, 
            'text':posting_text, 'title':posting_title, 'url':url}


def print_posting(post):
    """
    Convenience function for printing a posting retrieved with
    get_posting_info.
    """
    template = "\n".join(["{title}","{date} ({time})",
                          "{url}","{email}","","{text}"])
    return template.format(**post)


def fetch_links_postings(place,subcat,db=None):
    """
    Given a place, fetches all the postings from the place page and gets their
    info.
    """
    DB = "entries.db"
    if db is None:
       db = sqlite3.connect(DB) 
    c = db.cursor()

    print("Fetching links for: {}".format(place))
    links = get_links(place,subcat)
    if links is not None:
        print("{} links found.".format(len(links)))
        for (link,title) in links:
            # Check for duplicates
            query = c.execute("SELECT title,date,url FROM entries WHERE url=?",
                              (link,))
            # If this isn't a verbatim dupe, store it
            if len(query.fetchall())==0:
                try:
                    print(" - "+title+"   "+link)
                except UnicodeEncodeError:
                    print(" - "+"(unicode error in title)"+link)
                posting = get_posting(link)
                posting_tuple= [posting[key] for key in
                                ['title','date','time','url','email','text'] if posting]
                c.execute("INSERT INTO entries VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                          posting_tuple)
                time.sleep(1)  # sleep to give the web server a break
                db.commit()
        return True




if __name__=="__main__":
    parser_description = "Scrapes postings from craigslist."
    parser = argparse.ArgumentParser(description=parser_description)

    parser.add_argument('-c','--category',action='append',
                        help='Categories to fetch data from.  E.g., computer '\
                             'gigs: cpg')

    parser.add_argument('-l','--location',action='append',
                        help='Locations to fetch data from.')

    parsed =  parser.parse_args()


    # By default, fetch from all locations
    if parsed.location is None:
        places = get_places() 
    else:
        places = parsed.location
    print("Fetching from {} locations.".format(len(places)))

    # By default, fetch computer gigs
    if parsed.category is None:
        categories = ['cpg']
    else:
        categories = parsed.category
    print("Fetching from {} categories: {}".format(len(categories),
                                                   ", ".join(categories)))

    # Loop through all the categories and locations
    for cat in categories:
        for (i,place) in zip(count(),places):
            if fetch_links_postings(place,cat) or i%10==0:
                # Sleep to make web server hate us a little less
                print("Give server a break...")
                time.sleep(5)


