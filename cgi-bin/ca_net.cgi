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
import MySQLdb as mdb
import numpy as np
import networkx as nx

def ca_net():
    #con = mdb.connect('bscb-teaching.cb.bscb.cornell.edu', 'asd223', '6194', 'adtest')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    stmt = """SELECT entrezA, entrezB from PPI
    INNER JOIN Ca_Pathways
    ON Ca_Pathways.gene_id
    IN (PPI.entrezA, PPI.entrezB)"""




    cur.execute(stmt)
    Results = cur.fetchall()  # fetch all rows into the Results array
    total = len(Results)
    #cur.execute("DROP TEMPORARY TABLE rec")
    entries = []
    return list(Results)

#assemble pp network
pp_ca = ca_net()

#build network graph with networkx

G = nx.Graph()
G.add_edges_from(pp_ca)

def deg_dist_plot():
    degs = {}
    for n in G.nodes():
        deg = G.degree(n)
        if deg not in degs:
            degs[deg] = 0
        degs[deg] += 1
    items = sorted(degs.items())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([k for (k,v) in items], [v for (k,v) in items], 'bo')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.ylabel("number of nodes")
    plt.xlabel("Degree")
    plt.title("Degree Distribution")
    fig.savefig("../images/plot.pdf", format = 'pdf')

deg_dist_plot()

print '''
<html>
<body>
<h1>CGI is working. Image should display below:</h1>
<img src="../images/plot.pdf">
<h1>Image should display above</h1>
</body>
</html>
'''