#!/usr/bin/python
#-------------------------------------
# print "Content-type: text/html"
# print
#-------------------------------------
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage
import cgitb
cgitb.enable()
import MySQLdb as mdb
import tempfile
import os

form = FieldStorage()
query = form.getfirst('Proteins', 0)
#query = 'KRAS; SP100; ARAF'


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

def make_nxG(ppi):
    G = nx.Graph()
    G.add_edges_from(ppi)
    return G

##need to modify for web output
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
    print """</div>
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
    print """</div>
                </div>
            </div>
        </div>
        </body></html>"""
##

custom_ppi = make_custom_net(query)

G = make_nxG(custom_ppi)

make_net_plot(custom_ppi)

page string = """
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
