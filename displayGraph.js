var distanceCalculator = function(link, index) {
  return 200/link.value;
}

var width = 1000,
    height = 800

var svg = d3.select('body').append('svg')
    .attr('width', width)
    .attr('height', height);

var force = d3.layout.force()
    .gravity(.05)
    .charge(-100)
    .friction(.2)
    .linkStrength(.1)
    .size([width, height])
    .linkDistance(distanceCalculator);

d3.json('graph.json', function(error, json) {
  if (error) throw error;

  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll('.link')
      .data(json.links)
    .enter().append('line')
      .attr('class', 'link');

  var node = svg.selectAll('.node')
      .data(json.nodes)
    .enter().append('g')
      .attr('r', 5)
      .attr('class', 'node')
      .call(force.drag);

  node.append('circle')
      .attr('r', 5);

  node.append('text')
      .attr('dx', 12)
      .attr('dy', '.35em')
      .text(function(d) { return d.name });

  force.on('tick', function() {
    link.attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

    node.attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; });
  });
});
