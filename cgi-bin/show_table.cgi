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

print('''Content-Type: text/html

<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

<html>
<head><title>Tables in cookbook Database</title></head>
<body>

<p>Tables in database:</p>
''')

# Connect to database, display table list, disconnect
con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
cur = con.cursor()

stmt = '''
  SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
  WHERE TABLE_SCHEMA = 'ASD223_db' ORDER BY TABLE_NAME
'''
cur.execute(stmt)
for (tbl_name, ) in cur:
  print("%s<br />" % tbl_name)
cur.close()
con.close()

# Print page trailer
print('''
</body>
</html>
''')
