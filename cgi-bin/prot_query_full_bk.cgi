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
#query = "KRAS;SP100;SUMO1;TRAF4;TP53BP2"
#IDtype = "symbol"
#ppdb = ['LIT13', 'HI14', 'YU11']

print """<!DOCTYPE html>
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
    <!--link href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/yeti/bootstrap.min.css" rel="stylesheet"-->
    <!--link href="theme.css" rel="stylesheet"-->
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="../../assets/js/ie-emulation-modes-warning.js"></script>
    <link rel="stylesheet" href="theme.css">
    <link rel="stylesheet" href="assets/css/formalize.css" />
    <!--link rel="stylesheet" href="assets/css/demo.css" /-->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="assets/js/jquery.formalize.js"></script>
    <style id="jsbin-css">
    p {
        margin-top: 2em;
        margin-bottom: 2em;
        line-height: 1.6em;
        font-size: 20px;
    }
    
    .jumbotron {
        text-align: center;
    }
    
    .jumbotron p {
        font-size: 20px;
        font-weight: normal;
    }
    
    .navbar-default .navbar-brand {
        font-size: 20px;
    }
    
    .navbar-default .navbar-brand,
    .navbar-default .navbar-nav > li > a {
        color: #333;
    }
    
    .btn {
        font-size: 20px;
    }
    </style>
</head>

<body>
    <div class="navbar navbar-default navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <a href="../" class="navbar-brand">Human interactome resource</a>
                <button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#navbar-main">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div>
            <div class="navbar-collapse collapse" id="navbar-main">
                <ul class="nav navbar-nav">
                    <li class="dropdown">
                        <a>Search</a>
                    </li>
                    <li>
                        <a>Data sets</a>
                    </li>
                    <li>
                        <a>Contact</a>x
                    </li>
                    <li>
                        <a>About</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>"""





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
            pair = (Results[0][1], qt)

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        con.close()
        return (Results, ann)
          # fetch all rows into the Results array






def get_prot_ann(q):
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt = """SELECT gene_id, symbol, uniprot_id, description
        FROM gene_master
        WHERE %s in (gene_id, symbol, uniprot_id)"""
    cur.execute(stmt, (q,))
    res = cur.fetchall()
    return res[0]




qt = parse_query(query)
my_ppi = []
nodes = set()
DbResults = {}


nodes = set()
network_data = {}
for q in qt:
    all_d = {}
    allres = my_query(q, IDtype, ppdb)
    qp = allres[1][1]
    all_d[qp] = {}
    all_d['annotation'] = allres[1]
    all_d['ints'] = {}
    for p in allres[0]:
        all_d['ints'][p[1]] = p
    network_data[qp] = all_d

#make network
for k in network_data.keys():
    for pintr in network_data[k]['ints'].keys():
        nodes.add(tuple(sorted([k, pintr])))




custm_ppi = list(nodes)

def make_nxG(ppi):
    G = nx.Graph()
    G.add_edges_from(ppi)
    return G







    print """
    <div class="container">
        <div class="row">
            <div class="col-md-10 col-md-offset-1">
                 <div class="heading">
                    <center><b>Proteins in query(n%s)</b> %s
                            <br><b>Number of interactors</b> %s
                            <div> </div>
                            <br><b>Network properties</b>
                            <br><Number of Network nodes</b> %s
                            <br><Number of Network edges</b> %s
                            <br><Average degree connectivity</b> %s
                            <br><Average clustering coefficient</b> 555
                            <div></div>
                           <br/>
                        </center>
                    </div>""" %(qtl, qt, nint, ns, ne, dcon)
    return





def make_net_plot(ppi):
    G = make_nxG(ppi)
    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot with Largest subgraph (inset)")
    plt.ylabel("degree")
    plt.xlabel("rank")
    # draw graph in inset
    plt.axes([0.45,0.45,0.45,0.45])
    Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    pos=nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
    plt.savefig('/home/local/CORNELL/asd223/final/images/plot.svg', format="svg")
    return


def make_tables(ppi, network_data):
	G = make_nxG(ppi)
	ns = G.number_of_nodes()
    #ne = G.number_of_edges()
    query_ps = network_data.keys()
    qtl = len(query_ps)
    nint = ns - qtl
    #avgc = nx.average_clustering(G)
    dcon = nx.average_degree_connectivity(G)
    btwc = nx.betweenness_centrality(G)
    print """
    	<div class="container">
        <div class="row">
            <div class="col-md-10 col-md-offset-1">
                 <div class="heading">
                    <center><b>Proteins of interest</b> %s
                            <br><b>Number of interactors</b> %s
                            <div> </div>
                            <br><Number of Network nodes</b> %s
                            <br><Number of Network edges</b> %s
                            <br><Average degree connectivity</b> %s
                            <br><Average clustering coefficient</b> 555
                            <div></div>
                           <br/>
                        </center>
                    </div>""" %(query_ps, nint, ns, ns, dcon)
                    
    print """
	<br><b>Network degree distribution with largest connected subgraph</b> 
    <img src="../images/plot.svg">"""
    
    for k, v in network_data.items():
        p1ann = network_data[k]['annotation']
        p2s =  network_data[k]['ints']
        ps = len(p2s)

        print """<div class="heading">
                        <center><b>Protein of Interest: %s (%s)</b>
                        <br><b>%s %s</b>
                        <br/><b>Number of interactors</b> %s
                        
						""" %(p1ann[1], p1ann[0], p1ann[2], p1ann[3], ps)

        print """<table class="table table-striped">
                <th>Gene ID</th><th>Symbol</th><th>Supporing data set</th><th>Description</th>
                <tr>"""

        for (a, b, c, d) in p2s.values():
            print "<td>%s</td>" % (a)
            print "<td>%s</td>" % (b)
            print "<td>%s</td>" % (d)
            print "<td>%s</td>" % (c)
            print "</tr>"
        print "</table>"
    return 







make_net_plot(custm_ppi)

make_table(custm_ppi, network_data)

