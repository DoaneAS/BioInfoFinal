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

import pandas as pd
stmt = """CREATE TEMPORARY TABLE rec select * from PPI
where "KRAS" IN (PPI.symbolA, PPI.symbolB);
SELECT * from gene_info INNER JOIN rec
WHERE gene_info.gene_id IN (rec.entrezA, rec.entrezB)"""

def my_query2(query, stmt):
    #con = mdb.connect('bscb-teaching.cb.bscb.cornell.edu', 'asd223', '6194', 'adtest')
    con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    cur = con.cursor()

    stmt = """CREATE TEMPORARY TABLE rec select * from PPI
        where "KRAS" IN (PPI.symbolA, PPI.symbolB)"""

    stmt2 = """SELECT * from gene_info INNER JOIN rec
        WHERE gene_info.gene_id IN (rec.entrezA, rec.entrezB)"""

    cur.execute(stmt)
    cur.execute(stmt2)
    Results = cur.fetchall()  # fetch all rows into the Results array
    total = len(Results)
    entries = []
    df = pd.DataFrame( [[ij for ij in i] for i in Results] )
    return df

df = my_query2("KRAS", stmt)

t1 = df.to_html()\
    .replace('<table border="1" class="dataframe">','<table class="table table-striped">')

print '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Interactions</h1>
        <!-- *** Section 1 *** --->
        <h2>Section 1: QUERY PROTEIN</h2>
        <h3>Reference table: stock tickers</h3>
        ''' + t1 + '''
    </body>
</html>
'''