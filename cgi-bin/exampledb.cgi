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

import tempfile
import os

form = FieldStorage()
#query= form.getfirst('Protein',0)
#organism= form.getfirst('Organism',0)
#int_type= form.getfirst('Interaction',0)


#dblit = form.getfirst('LIT',0)
dblit = form.getvalue('DB')
#dbyu = form.getfirst('DB',0)
#dbhi = form.getfirst('DB',0)

print dblit
print '''
<html>
    <body>
        <h1>This is a test page.</h1>

        <h2>You selected %s</h2>
    </body>
</html>''' %(dblit)