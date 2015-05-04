#!/usr/bin/python
#-------------------------------------
# print "Content-type: text/html"
# print
#-------------------------------------
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage
import cgitb
cgitb.enable()
import MySQLdb as mdb
import tempfile
import os

form = FieldStorage()
query = form.getfirst('Protein', 0)
#query = 'KRAS; SP100; ARAF'


print """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="jumbotron-narrow.css">
</head>
"""


def my_query(prot_query):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    try:
        #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
        cur = con.cursor()

        stmt = """select gene_id, symbol, description from gene_info INNER JOIN PPI
                    where PPI.entrezA = gene_info.gene_id AND %s = PPI.symbolB
                    UNION
                    select gene_id, symbol, description from gene_info INNER JOIN PPI
                    where PPI.entrezB = gene_info.gene_id AND %s = PPI.symbolA"""

        #cur.execute("""DROP TEMPORARY TABLE IF EXISTS REC""")
        cur.execute(stmt, (prot_query,prot_query))

        Results = cur.fetchall()  # fetch all rows into the Results array

        print """<html><h3> %s protein interactions</h1>
                    <head><title>Interactions with  ..query.. </title></head>
                    <body>
                    <p>are:</p>""" %(prot_query)

        print  """<table class="table table-striped">
                <th>Gene ID</th><th>Symbol</th><th>Description</th>
                <tr>"""

        for (a, b, c) in Results:
            print "<td>%s</td>" % (a)
            print "<td>%s</td>" % (b)
            print "<td>%s</td>" % (c)
            print "</tr>"
        print "</table>"

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        con.close()

query = query.replace(' ', '')
qt = query.split(";")
for q in qt:
    d = my_query(q)


print """
</body>
<address>
  <strong>Ashley S Doane</strong><br>
  BTRY 6381<br>
  <a href="mailto:#">asd223@cornell.edu</a>
</address>
</html>
"""
