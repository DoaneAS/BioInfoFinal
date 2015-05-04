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
import tempfile
import os

form = FieldStorage()
query= form.getfirst('Protein',0)

print '''
<!DOCTYPE html>
<html lang="en">
<div class="container-fluid">
  ...
</div>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

<html>
<h3> interactions with  ..query..</h1>
<head><title>Interactions with  ..query.. </title></head>
<body>

<p>are:</p>
'''

def my_query2(prot_query):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    cur = con.cursor()

    stmt = "CREATE TEMPORARY TABLE rec select * from PPI where %s IN (PPI.symbolA, PPI.symbolB)"


    stmt2 = """SELECT DISTINCT gene_id, symbol, description from gene_info INNER JOIN rec
        WHERE gene_info.gene_id IN (rec.entrezA, rec.entrezB)"""

    try:
        cur.execute("""DROP TEMPORARY TABLE IF EXISTS REC""")
        cur.execute(stmt, (prot_query,))
        cur.execute(stmt2)

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    Results = cur.fetchall()  # fetch all rows into the Results array
    total = len(Results)
    #cur.execute("DROP TEMPORARY TABLE rec")
    entries = []

    print '''<table class="table table-striped">
            <th>Gene ID</th><th>Symbol</th><th>Description</th>
        <tr>'''
    for (a, b, c) in Results:
        print "<td>%s</td>" %(a)
        print "<td>%s</td>" %(b)
        print "<td>%s</td>" %(c)
        print "</tr>"
    print "</table>"
    #cur.execute("DROP TEMPORARY TABLE rec")

    finally:

        if con:
            con.close()



##parse form data and loop through mysql query fx
qt = query.split(';')
for q in qt:
    my_query2(q)


print '''
</body>
<address>
  <strong>Ashley S Doane</strong><br>
  BTRY 6381<br>
  <a href="mailto:#">asd223@cornell.edu</a>
</address>
</html>
'''