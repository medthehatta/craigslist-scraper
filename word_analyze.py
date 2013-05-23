from pandas.io.sql import frame_query
from collections import Counter
from itertools import count
import sqlite3
import re
import pickle

try:
    # Check to see if we have a pickle file already
    corpus = pickle.load(open("text_corpus.pkl",'rb'))
    sub_texts = pickle.load(open("sub_texts.pkl",'rb'))

    print("Data loaded from pickle files.")

    # Get the database data
    db = sqlite3.connect('entries.db')
    df = frame_query('select * from entries',db)


except Exception:

    print("Data not found.  Regenerating histograms...")

    # Initialize the storage
    texts = Counter()
    sub_texts={}
    titles=Counter()
    sub_title={}

    records = df[['id','title','text']].T
    records_len = len(records)

    # Initialize the "word" regexp
    words_rx = re.compile(r'[a-zA-Z\-]+')

    # Compute all the histograms
    for (i,(id,title,text)) in zip(count(),records.iteritems()):
        sub_texts[id] = word_histogram(text,[texts])
        sub_title[id] = word_histogram(title,[titles,texts])
        if i%100==0: print("{}/{}".format(i,records_len))

    print("Histograms generated.  Saving...")

    # Save the result!
    with open("text_corpus.pkl",'wb') as f:
        pickle.dump(corpus,f)
    with open("sub_texts.pkl",'wb') as f:
        pickle.dump(sub_texts,f)
    with open("sub_titles.pkl",'wb') as f:
        pickle.dump(sub_title,f)

    print("Done.")


def word_histogram(text,contexts):
    """
    Makes a histogram of the words in a text, and includes the word counts in
    global contexts.
    """
    word_list = re.findall(r'[a-zA-Z\-]+', str(text).lower())
    word_histogram = Counter(word_list) 

    for context in contexts:
        context += word_histogram

    return word_histogram



def idf(num,den):
    """
    Divides two counters by each other.  All the items in ``num`` must be
    present in ``den``, but the converse doesn't need to be true. 

    Returns: sorted list of most inordinately frequent items in ``num``
    compared to ``den``.
    """
    max_den = max(list(den.values()))

    vals = []
    for k in num:
        vals.append([num[k]/float(den[k]),k])

    return [a[1] for a in sorted(vals,key=lambda x:-x[0])]

        

