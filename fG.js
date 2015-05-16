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
        
    // load the JSON file.
    d3.json("graph.json", function(error, graph) {

        force.nodes(graph.nodes)
            .links(graph.links)
            .start();


        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link");

        // create a <circle> SVG element for each node
        // in the graph, and specify attributes.
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

        // The name of each node is the node number.
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