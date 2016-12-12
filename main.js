let minYear = 2010;
let maxYear = 2020;
let numStates = 18;

var width = 960,
  height = 500,
  centered;

// Define color scale
var colorScale = d3.scale.category20();

// Center the Map in Boston
var projection = d3.geo.mercator()
  .scale(35500)
  .center([-71, 42.4])
  .translate([width / 2, height / 2]);

var path = d3.geo.path()
  .projection(projection);

// Set svg width & height
var svg = d3.select('svg')
  .attr('width', width)
  .attr('height', height);

// Add background
svg.append('rect')
  .attr('class', 'background')
  .attr('width', width)
  .attr('height', height)

var g = svg.append('g');

var effectLayer = g.append('g')
  .classed('effect-layer', true);

var mapLayer = g.append('g')
  .classed('map-layer', true);

var neighborhoodLayer = g.append('g')
  .classed('neighborhood-layer', true);

var dummyText = g.append('text')
  .classed('dummy-text', true)
  .attr('x', 10)
  .attr('y', 30)
  .style('opacity', 0);

var bigText = g.append('text')
  .classed('big-text', true)
  .attr('x', 20)
  .attr('y', 45);

var yearIndex = 0;

// Load map data
d3.json('data/boston.json', function(error, boundaryData){
  // Draw each province as a path
  mapLayer.selectAll('path')
    .data(boundaryData.features)
    .enter().append('path')
    .attr('d', path)
    .attr('vector-effect', 'non-scaling-stroke')
    .style('fill', "#A8DBA8")
});

d3.json('data/gent-geodata.geojson', function(error, gentGeoData) {
  maxYear = gentGeoData['maxYear'];
  minYear = gentGeoData['minYear'];
  numStates = gentGeoData['numStates'];

  document.getElementById('yearSlider').setAttribute('min', minYear);
  document.getElementById('yearSlider').setAttribute('max', maxYear);

  neighborhoodLayer.selectAll('path')
  .data(gentGeoData.features)
  .enter().append('path')
  .attr('d', path)
  .attr('vector-effect', 'non-scaling-stroke')
  .attr('fill', (d) => colorScale(d.properties.states[0]))
})

function setYear(year=minYear) {
  yearIndex = year - minYear;
  if (yearIndex < 0 || yearIndex > maxYear-minYear) {
    console.error("Year out of range!");
    return;
  }

  neighborhoodLayer.selectAll('path')
    .attr('fill', (d) => colorScale(d.properties.states[yearIndex]))
}
