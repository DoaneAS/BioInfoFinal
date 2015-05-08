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
import networkx as nx

form = FieldStorage()
#query = form.getfirst('Proteins', 0)
#query = 'KRAS; SP100; ARAF'
print os.getcwd()

print """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="jumbotron-narrow.css">
</head>
"""

def make_custom_net(query):
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt = """SELECT DISTINCT entrezA, entrezB from PPI WHERE
        %s IN (PPI.symbolA, PPI.symbolB)"""
    custom_ppi = set()
    qt = query.replace(' ','')
    qt = qt.split(";")
    for q in qt:
        cur.execute(stmt, (q,))
        res = list(cur.fetchall())
        for pp in res:
            custom_ppi.add(tuple(sorted(pp)))
    return list(custom_ppi)


def get_ca_genes():
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    stmt = """SELECT gene_id from Ca_Pathways"""
    cur.execute(stmt,)
    res = cur.fetchall()
    cag = set([c[0] for c in res])
    return cag

ca_genes = get_ca_genes()


def make_ca_net():
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
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

pp_ca = make_ca_net()

def get_ca_paths():
    #con = mdb.connect('bscb-teaching.cb.bscb.cornell.edu', 'asd223', '6194', 'adtest')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    stmt = """SELECT DISTINCT pathway from Ca_Pathways"""

    cur.execute(stmt)
    Results = cur.fetchall()  # fetch all rows into the Results array
    #cur.execute("DROP TEMPORARY TABLE rec")
    entries = []
    return list(Results)

res = get_ca_paths()
paths = []
for i in res:
    paths.append(i[0])


#construct networks for each pathway

def make_net_by_path(paths):
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
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

nps = make_net_by_path(paths)

path_graphs = {}
for p in nps.keys():
    net = nps[p]
    G = nx.Graph()
    G.add_edges_from(net)
    path_graphs[p] = G

G = path_graphs['DNA Damage Control']
import json
from networkx.readwrite import json_graph
data = json_graph.node_link_data(G)
with open('../wdata/graph.json', 'w') as f:
    json.dump(data, f, indent=4)


page_string = """
<html>
<body>
        <div id="d3-fG"></div>
        <style>
        .node {stroke: #fff; stroke-width: 1.5px;}
        .link {stroke: #999; stroke-opacity: .6;}
        </style>

<script>
require.config({paths: {d3: "http://d3js.org/d3.v3.min"}});
require(["d3"], function(d3) {
    var width = 300,
        height = 300;

    var color = d3.scale.category10();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#d3-fG").select("svg")
    if (svg.empty()) {
        svg = d3.select("#d3-fG").append("svg")
                    .attr("width", width)
                    .attr("height", height);
    }


    d3.json("graph.json", function(error, graph) {

        force.nodes(graph.nodes)
            .links(graph.links)
            .start();


        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link");


        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)  // radius
            .style("fill", function(d) {
                // The node color depends on the pathway.
                return color(d.pathway);
            })
            .call(force.drag);


        node.append("title")
            .text(function(d) { return d.id; });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    });
});
</script>

</body>
</html>

"""

print """
<html>
<body>
<address>
  <strong>Ashley S Doane</strong><br>
  BTRY 6381<br>
  <a href="mailto:#">asd223@cornell.edu</a>
</address>
</body>
</html>
"""
