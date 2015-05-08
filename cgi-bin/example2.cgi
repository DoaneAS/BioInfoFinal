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


form = FieldStorage()
query= form.getfirst('Protein',0)
organism= form.getfirst('Organism',0)
int_type= form.getfirst('Interaction',0)


#got to mysql query here



def my_query(query):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    stmt = """
        select * from PPI
        where "KRAS" IN (PPI.symbolA, PPI.symbolB)"""

    cur.execute(stmt)


    for (x,) in cur:
        x = str(x)
    url = "/cgi-bin/example2.py?phrase=" + urllib.quote(x)
    label = cgi.escape(x, 1)
    print('<a href="%s">%s</a><br />' % (url, label))



print '''
<html>
    <body>
        <h1>This is a test page.</h1>
        <h2>Your query was: %s</h2>
        <h2>You selected the oragnism: %s</h2>
        <h2>You wanted the interaction type: %s</h2>
    </body>
</html>''' %(query, organism, int_type)