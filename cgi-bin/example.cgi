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
query= form.getfirst('Protein',0)
organism= form.getfirst('Organism',0)
int_type= form.getfirst('Interaction',0)

print '''
<html>
    <body>
        <h1>This is a test page.</h1>
        <h2>Your query was: %s</h2>
        <h2>You selected the oragnism: %s</h2>
        <h2>You wanted the interaction type: %s</h2>
    </body>
</html>''' %(query, organism, int_type)