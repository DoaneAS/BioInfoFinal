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
import cStringIO

def ca_net():
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
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


pp_ca = ca_net()

#assemble pp network

#get the different pathways
def ca_net_path():
    #con = mdb.connect('bscb-teaching.cb.bscb.cornell.edu', 'asd223', '6194', 'adtest')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    stmt = """SELECT DISTINCT pathway from Ca_Pathways"""

    cur.execute(stmt)
    Results = cur.fetchall()  # fetch all rows into the Results array
    #cur.execute("DROP TEMPORARY TABLE rec")
    entries = []
    return list(Results)

res = ca_net_path()
paths = []
for i in res:
    paths.append(i[0])


#construct networks for each pathway

def net_by_path(paths):
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    path_nets = {}
    for path in paths:
        stmt = """SELECT entrezA, entrezB from PPI
        INNER JOIN Ca_Pathways
        ON Ca_Pathways.gene_id
        IN (PPI.entrezA, PPI.entrezB)
        AND Ca_Pathways.pathway = %s"""

        cur.execute(stmt, (path,))

        results = list(cur.fetchall())
        path_nets[path] = results
    return path_nets

nps = net_by_path(paths)


#build network graph with networkx

path_graphs = {}
for p in nps.keys():
    net = nps[p]
    G = nx.Graph()
    G.add_edges_from(net)
    path_graphs[p] = G


for pg in path_graphs.keys():
    degs = {}
    g = path_graphs[pg]
    for n in g.nodes():
        deg = g.degree(n)
        if deg not in degs:
            degs[deg] = 0
        degs[deg] += 1
    items = sorted(degs.items())
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111)
    ax.plot([k for (k,v) in items], [v for (k,v) in items], 'bo')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.ylabel("number of nodes")
    plt.xlabel("Degree")
    plt.title("Degree Distribution for %s" %pg)
    tit = str(pg)[0:2]


    #plot to file
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)
    print "Content-Type: text/html\n"
    print """<body>
        <div class="section">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <img src="data:image/png;base64,%s"/>""" % sio.getvalue().encode("base64").strip()
    print """"</div>
                </div>
            </div>
        </div>"""

    fig = plt.figure(figsize=(4,4))
    g = path_graphs[pg]
    pos=nx.spring_layout(g,iterations=20)
    nx.draw(g,pos, node_size=30, width=0.5)
    tit = str(pg)[0:2]
    plt.title("%s Network" %pg)
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)
    #fig.savefig("degree_distribution%s.pdf" %tit, format = 'pdf')

    print """<body>
        <div class="section">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <img src="data:image/png;base64,%s"/>""" % sio.getvalue().encode("base64").strip()
    print """"</div>
                </div>
            </div>
        </div>
        </body></html>"""



#     #network graph
# for pg in path_graphs.keys():
#     fig = plt.figure(figsize=(4,4))
#     g = path_graphs[pg]
#     pos=nx.spring_layout(g,iterations=20)
#     nx.draw(g,pos, node_size=30, width=0.5)
#     tit = str(pg)[0:2]
#     plt.title("%s Network" %pg)

#     format = "png"
#     sio = cStringIO.StringIO()
#     plt.savefig(sio, format=format)
#     #fig.savefig("degree_distribution%s.pdf" %tit, format = 'pdf')

#     #network graph
#     print """<html><body>Interaction network for %s pathway genes""" %pg
#     print """<img src="data:image/png;base64,%s"/>
#     </body></html>""" % sio.getvalue().encode("base64").strip()

