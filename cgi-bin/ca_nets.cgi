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

def make_ca_net():
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    cur = con.cursor()

    stmt = """SELECT entrezA, entrezB from MASTER_P
    INNER JOIN Ca_Pathways
    ON Ca_Pathways.gene_id
    IN (MASTER_P.entrezA, MASTER_P.entrezB)"""

    cur.execute(stmt)
    Results = cur.fetchall()  # fetch all rows into the Results array
    total = len(Results)
    #cur.execute("DROP TEMPORARY TABLE rec")
    entries = []
    return list(Results)


pp_ca = make_ca_net()

#assemble pp network

#get the different pathways
def get_ca_paths():
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

res = get_ca_paths()
paths = []
for i in res:
    paths.append(i[0])


#construct networks for each pathway

def make_net_by_path(paths):
    #con = mdb.connect(host='127.0.0.1', port=3307, user='asd223', passwd='5NKEAP', db='ASD223_db')
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()

    path_nets = {}
    for path in paths:
        stmt = """SELECT entrezA, entrezB from MASTER_P
        INNER JOIN Ca_Pathways
        ON Ca_Pathways.gene_id
        IN (MASTER_P.entrezA, MASTER_P.entrezB)
        AND Ca_Pathways.pathway = %s"""

        cur.execute(stmt, (path,))

        results = list(cur.fetchall())
        path_nets[path] = results
    return path_nets

nps = make_net_by_path(paths)


#build network graph with networkx

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
with open("/home/local/CORNELL/asd223/final/images/graph.json", 'w') as f:
    json.dump(data, f, indent=4)

pagestring= """<html>
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


    d3.json("/home/local/CORNELL/asd223/final/images/graph.json", function(error, graph) {

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
</html>"""

print pagestring

# path_graphs = {}
# for p in nps.keys():
#     net = nps[p]
#     G = nx.Graph()
#     G.add_edges_from(net)
#     path_graphs[p] = G


# for pg in path_graphs.keys():
#     degs = {}
#     g = path_graphs[pg]
#     for n in g.nodes():
#         deg = g.degree(n)
#         if deg not in degs:
#             degs[deg] = 0
#         degs[deg] += 1
#     items = sorted(degs.items())
#     fig = plt.figure(figsize=(4,4))
#     ax = fig.add_subplot(111)
#     ax.plot([k for (k,v) in items], [v for (k,v) in items], 'bo')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     plt.ylabel("number of nodes")
#     plt.xlabel("Degree")
#     plt.title("Degree Distribution for %s" %pg)
#     tit = str(pg)[0:2]


#     #plot to file
#     print """<body>
#         <div class="section">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <img src="/home/local/CORNELL/asd223/final/images/plot.png">"""
#     print """</div>
#                 </div>
#             </div>
#         </div>"""

#     fig = plt.figure(figsize=(4,4))
#     g = path_graphs[pg]
#     pos=nx.spring_layout(g,iterations=20)
#     nx.draw(g,pos, node_size=30, width=0.5)
#     tit = str(pg)[0:2]
#     plt.title("%s Network" %pg)
#     format = "png"
#     #sio = cStringIO.StringIO()
#     #plt.savefig(sio, format=format)
#     plt.savefig('/home/local/CORNELL/asd223/final/images/plot.png')
#     #fig.savefig("degree_distribution%s.pdf" %tit, format = 'pdf')

#     print """<body>
#         <div class="section">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                     <img src="/home/local/CORNELL/asd223/final/images/plot.png">
#                     </div>
#                     </div>
#                     </body></html>"""




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

