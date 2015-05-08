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

import numpy as np
import tempfile
import os
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


import networkx as nx
form = FieldStorage()
query = form.getfirst('Protein', 0)
IDtype = form.getfirst('IDtype')
ppdb = form.getvalue('ppdb')
#query = 'KRAS; SP100; ARAF'


print """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head
        content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">
    <title>Human protein interactome explorer</title>
    <!-- Latest compiled and minified
        CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    <!-- Custom styles for this template -->
    <!--link href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/flatly/bootstrap.min.css" rel="stylesheet"-->


    <link href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/paper/bootstrap.min.css" rel="stylesheet">


</head>
"""







def uniprot2gene(query):
    q = query
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt= """SELECT gene_id from gene2uniprot WHERE uniprot_id = %s"""
    cur.execute(stmt, (q,))
    res = cur.fetchall()
    return res


geneids = []
#for q in qt:
#    geneids.append(uniprot2gene(q)[0][0])

def parse_query(query):
    #returns query ids in list
    query = query.replace(' ', '')
    qt = query.split(";")
    return qt




def uniprot2gene(query):
    q = query
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt= """SELECT gene_id from gene2uniprot WHERE uniprot_id = %s"""
    cur.execute(stmt, (q,))
    res = cur.fetchall()[0][0]
    return res



def get_ppdb(ppdb):
    dbs = ','.join(ppdb)
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    cur = con.cursor()
    cur.execute("""DROP TABLE IF EXISTS PPI""")

    cur.execute("""CREATE TABLE PPI like MASTER_P""")

    stmt_db = """INSERT IGNORE INTO PPI SELECT * from MASTER_P WHERE FIND_IN_SET(%s,PPDB)"""

    for p in ppdb:
        cur.execute(stmt_db, (p,))
    return


def my_query(qt, IDtype, ppdb):
    #get info on query gene
    ann = get_prot_ann(qt)

    #set up PPI table with indicated databases
    get_ppdb(ppdb)

    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    try:
        #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
        cur = con.cursor()

        stmt_s = """select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezA = gene_info.gene_id AND %s = PPI.symbolB
                    UNION
                    select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezB = gene_info.gene_id AND %s = PPI.symbolA"""

        stmt_e = """select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezA = gene_info.gene_id AND %s = PPI.entrezB
                    UNION
                    select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezB = gene_info.gene_id AND %s = PPI.entrezA"""

        stmt_u = """select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezA = gene_info.gene_id AND %s = PPI.uniprotB
                    UNION
                   select gene_id, symbol, description, ppdb from gene_info INNER JOIN PPI
                    where PPI.entrezB = gene_info.gene_id AND %s = PPI.uniprotA"""

        #cur.execute("""DROP TEMPORARY TABLE IF EXISTS REC""")

        if IDtype == 'entrez':
            cur.execute(stmt_e, (qt, qt))
            Results = cur.fetchall()
            pair = (Results[0][0], qt)

        elif IDtype == 'symbol':
            cur.execute(stmt_s, (qt, qt))
            Results = cur.fetchall()
            pair = (Results[0][1], qt)

        elif IDtype == 'uniprot':
            cur.execute(stmt_u, (qt, qt))
            Results = cur.fetchall()

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        con.close()
        return pair
          # fetch all rows into the Results array






def get_prot_ann(q):
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt = """SELECT gene_id, symbol, uniprot_id, description
        FROM gene_master
        WHERE %s in (gene_id, symbol, uniprot_id)"""
    cur.execute(stmt, (q,))
    res = cur.fetchall()[0]
    return res




qt = parse_query(query)
my_ppi = []
nodes = set()
for q in qt:
    res = my_query(q, IDtype, ppdb)
    nodes.add(tuple(sorted([res[0], res[1]])))

nodes = set()
for q in qt:
    res = my_query(q, IDtype, ppdb)
    p2 = res[1]
    for r in res[0]:
        #nodes.add(tuple(sorted([p2, r[0]])
        nodes.add(tuple(sorted([r[0], p2])))

custm_ppi = list(nodes)

def make_nxG(ppi):
    G = nx.Graph()
    G.add_edges_from(ppi)
    return G

def get_net_stats(ppi):
    G = nx.Graph()
    G.add_edges_from(ppi)



def make_net_plot(ppi):
    G = make_nxG(ppi)
    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    # draw graph in inset
    plt.axes([0.45,0.45,0.45,0.45])
    Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    pos=nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

    plt.savefig('/home/local/CORNELL/asd223/final/images/plot.png')

    print '''
    <html>
    <body>
    <h1>CGI is working. Image should display below:</h1>
    <img src="../images/plot.png">
    <h1>Image should display above</h1>
    </body>
    </html>
    '''


make_net_plot(custm_ppi)



