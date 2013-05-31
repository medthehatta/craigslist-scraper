import sqlite3
from pandas.io.sql import read_frame
import sys

if __name__=='__main__':
    db = sqlite3.connect('entries.db') 
    query_template = ("SELECT id,title,url,date(date) "
                      "FROM entries "
                      "WHERE date(date)>date('now','-5 day') "
                      "AND text LIKE '%{}%'"
                      "ORDER BY date(date)")
    c = db.cursor()
    
    if len(sys.argv)>1:
        keywords = sys.argv[1:]
    else:
        keywords = [""]

    for keyword in keywords:
        print()
        print(">>> {}".format(keyword))
        df = c.execute(query_template.format(keyword))
        da = df.fetchall()

        for line in da:
            (id,title,url,date) = line
            try:
                print("({}) {}\n  {} - {}".format(id,url,title,date))
            except UnicodeEncodeError:
                print("({}) {}\n  {} - {}".format(id,url,"[unicode error]",date))
                
            


