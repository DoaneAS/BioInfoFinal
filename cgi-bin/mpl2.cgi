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
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import random

x = [random.random() for i in range(10)]
y = [random.random() for i in range(10)]

plt.scatter(x,y)
#plt.savefig('../images/plot.png')

import cStringIO #I think I will need this but not sure how to use


format = "png"
sio = cStringIO.StringIO()
plt.savefig(sio, format=format) #plot from above
print "Content-Type: image/%s\n" % format
#msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY) # Needed this on windows, IIS
sys.stdout.write(sio.getvalue())


print """<html><body>
...a bunch of text and html here...
<img src="data:image/png;base64,%s"/>
...more text and html...
</body></html>""" % sio.getvalue().encode("base64").strip()