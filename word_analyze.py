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

except Exception:

    print("Data not found.  Regenerating histograms...")

    # Get the data
    db = sqlite3.connect('entries.db')
    df = frame_query('select * from entries',db)

    # Initialize the storage
    corpus=Counter()
    sub_texts={}

    # Retrieve id and text only
    id_and_text_0 = df[['id','text']].T
    len_id_and_text = len(id_and_text_0)
    id_and_text = id_and_text_0.iteritems()

    # Initialize the "word" regexp
    words_rx = re.compile(r'[a-zA-Z\-]+')

    # Compute all the histograms
    for (i,(id,text)) in zip(count(),id_and_text):
        word_list = words_rx.findall(str(text).lower())
        sub_text=Counter(word_list)
        sub_texts[id]=sub_text
        corpus+=sub_text
        if i%100==0: print("{}/{}".format(i,len_id_and_text))

    print("Histograms generated.  Saving...")

    # Save the result!
    with open("text_corpus.pkl",'wb') as f:
        pickle.dump(corpus,f)
    with open("sub_texts.pkl",'wb') as f:
        pickle.dump(sub_texts,f)

    print("Done.")



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
        d = den.get(k) 
        if d is None: raise KeyError("den does not contain {}".format(k))
        vals.append([num[k]/float(d),k])

    return [a[1] for a in sorted(vals,key=lambda x:-x[0])]

        

