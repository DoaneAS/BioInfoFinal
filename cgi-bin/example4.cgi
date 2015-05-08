#!/usr/bin/python
#-------------------------------------
print "Content-type: text/html"
print
#-------------------------------------
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage
import cgitb
cgitb.enable()
import MySQLdb as mdb

import urllib
import cgi

def my_query(query):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    stmt = """
        select * from PPI
        where "KRAS" IN (PPI.symbolA, PPI.symbolB)"""

    cur.execute(stmt)
    Results = cur.fetchall()  # fetch all rows into the Results array
    total = len(Results)
    entries = []

    if total < 1:
        print "There weren’t any interactions!"

    else:
        for record in range(total):
            entry = {}  # a blank dictionary to hold each record
            entry["id"] = Results[record][0]  # field 0 = guestbook ID
            entry["gid"] = Results[record][1] # field 1 = timestamp
            entry["q"] = Results[record][4]  # and so on…
            entry["int"] = Results[record][5]
            entries.append(entry)  # add this entry to the master list

    ### parse variables into table
    for entry in entries:
        print "<LI>" + entry["gid"] + ' ' + entry["q"] + ' ' + entry['int']