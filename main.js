
window.addEventListener("load", run);


function run () {

    // world-topo.json is a GeoJSON file, not a TopoJSON file
    // so there's nothing special to be done

    d3.json("world-topo.json", function(error,topology) {
  attachVALToWorldData(topology,data_values);
  drawMap(topology);
    });
}



/*
 * Attach country values to the world data
 * 
 */

function attachVALToWorldData (world,data) {

    var features = world.features;
    var f;

    for (var i=0; i<features.length; i++) {
  f = hasVAL(features[i].id,data);
  if (f) {
      features[i]["hasVAL"] = true;
      features[i]["VAL"] = f;
  } else {
      features[i]["hasVAL"] = false;
  }
    }
}


function hasVAL (code,data) {

    for (var i=0;i<data.length; i++) {
  if (data[i][0] === code) {
      return data[i][2];
  }
    }
    return false;
}





var data_values = [
    ["USA",'US', 71],
    ["CHN",'China',51],
    ["JPN",'Japan',50],
    ["GBR",'UK',45],
    ["KOR",'South Korea',44],
    ["NOR",'Norway',42],
    ["CAN",'Canada',42],
    ["SWE",'Sweden',42],
    ["NLD",'Netherlands',41],
    ["DEU",'Germany',41],
    ["SGP",'Singapore',40],
    ["DNK",'Denmark',40],
    ["CHE",'Switzerland',39],
    ["FRA",'France',39],
    ["AUS",'Australia',39],
    ["FIN",'Finland',39],
    ["NZL",'New Zealand',38],
    ["LUX",'Luxembourg',36],
    ["BEL",'Belgium',33],
    ["AUT",'Austria',33],
    ["IND",'India',31],
    ["HKG",'Hong Kong',31],
    ["ARE",'United Arab Emirates',30],
    ["ISR",'Israel',30],
    ["IRL",'Ireland',29],
    ["POL",'Poland',29],
    ["RUS",'Russia',29],
    ["TWN",'Taiwan',28],
    ["HUN",'Hungary',27],
    ["BRA",'Brazil',27],
    ["CZE",'Czech Republic',27],
    ["ESP",'Spain',27],
    ["MYS",'Malaysia',25],
    ["ITA",'Italy',25],
    ["VNM",'Vietnam',24],
    ["TUR",'Turkey',23],
    ["CHL",'Chile',23],
    ["IDN",'Indonesia',23],
    ["PRT",'Portugal',21],
    ["MEX",'Mexico',21],
    ["SAU",'Saudi Arabia',21],
    ["PHL",'Philippines',21],
    ["BGR",'Bulgaria',20],
    ["THA",'Thailand',20],
    ["ROU",'Romania',19],
    ["COL",'Colombia',19],
    ["PER",'Peru',19],
    ["GRC",'Greece',19],
    ["EGY",'Egypt',18],
    ["ZAF",'South Africa',18],
    ["VEN",'Venezuela',18],
    ["ARG",'Argentina',17],
    ["KEN",'Kenya',17],
    ["NGA",'Nigeria',16],
    ["UKR",'Ukraine',15]
]



/*
 * BROWSER SIZE
 *
 */

function availableWidth () {
    return Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
}

function availableHeight () {
    return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
}



/* 
 * COLORS
 *
 */

var color_CountryBaseVAL = "#80cbec";
var color_background = "#003a5b";
var highlightColor = "#a4d15e";

var saved_height = 0;
var saved_width = 0;



/* 
 * ON MOUSE OVER A COUNTRY
 *
 */

function highlightCountry (elt) {
    elt.setAttribute("data-saved-fill",elt.style["fill"]);
    elt.setAttribute("data-saved-opacity",elt.style["fill-opacity"]);
    elt.style["fill-opacity"] = "1";
    elt.style.fill = highlightColor;
    var h = saved_height/4;
    var w = saved_width/5;
    drawIndexTileElt(d3.select("#svg-map"),
                     0,saved_height-h,w,h,elt)
}

function normalizeCountry (elt) {
    elt.style.fill = elt.getAttribute("data-saved-fill"); //color_CountryBaseVAL;
    elt.style["fill-opacity"] = elt.getAttribute("data-saved-opacity");
    d3.select("#index_tile_on_map").remove();
    
}

function drawIndexTileElt (svg,x,y,width,height,elt) {
    
    var g = svg.append("g")
  .attr("id","index_tile_on_map");
    
    g.append("text")
  .attr("x",x+width-20)
  .attr("y",y+height/2)
  //.attr("dy","0.35em")
  .attr("text-anchor","end")
  .attr("font-family","sans-serif")
  .attr("font-size",(0.6*height)+"px")
  .attr("font-weight","bold")
  .text(elt.getAttribute("data-val")+"%")
  .attr("fill",highlightColor);

    g.append("text")
  .attr("x",x+width-20)
  .attr("y",y+height/2)
  .attr("dy","1.35em")
  .attr("text-anchor","end")
  .attr("font-family","sans-serif")
  .attr("font-size",(0.18*height)+"px")
  .attr("font-weight","bold")
  .text(elt.getAttribute("data-country-name").toUpperCase())
  .attr("fill",highlightColor);
}



/*
 * DRAW THE MAP
 * 
 */

function drawMap (world) {

    console.log(world.features);

    /* size to fill the space but keep aspect ratio */

    var availWidth = availableWidth()-50;
    var availHeight = availableHeight()-50;
    
    var mapWidth = 760;
    var mapHeight = 380;

    var scaleH = availHeight / mapHeight;
    var scaleW = availWidth / mapWidth;

    var scale = Math.min(scaleH,scaleW);

    var height = scale * mapHeight;
    var width = scale * mapWidth;

    saved_height = height;
    saved_width = width;
    
    var svg = d3.select("#svg-map")
  .attr("x",0)
  .attr("y",0)
  .attr("width", width)
  .attr("height", height)
    
    var g = svg.append("g")
  .attr("transform","scale("+scale+"),translate(-100,0)");

    var projection = d3.geo.mercator()
  .center([0, 0 ])
  .scale(100)
  .rotate([0,0]);
    
    var path = d3.geo.path()
  .projection(projection);

    var max_VAL = d3.max(data_values,function (r) { return r[2]; });

    var country = g.selectAll(".country")   // select country objects (which don't exist yet)
  .data(world.features)  // bind data to these non-existent objects
  .enter()
  .append("path") // prepare data to be appended to paths
  .attr("class", "country")
  .attr("id", function(d) { return "code_" + d.id; })  // give each a unique id, just in case
  .attr("d", path) // create them using the svg path generator defined above
        // color each country based on VAL (set to opacity 0 if no VAL)
  .style("fill", color_CountryBaseVAL)
        .style("fill-opacity",function(d) {if (d.hasVAL) { return d.VAL / max_VAL; } else { return 0; } })
  // store country name and value as data-attributes so highlightCountry can access them
  .attr("data-country-name", function(d) {if (d.hasVAL) { return shorten(d.properties.name); }})
  .attr("data-val", function(d) {if (d.hasVAL) { return d.VAL; }})
  // event handlers
  .on("mouseover", function(d) {if (d.hasVAL) { highlightCountry(this); }})
  .on("mouseout", function(d) {if (d.hasVAL) { normalizeCountry(this); }})


    // hide antarctica (maybe not needed...)
    d3.select("#code_ATA")
        .attr("visibility","hidden");

}


function shorten (name) {
    if (name==="United States of America") {
  return "USA";
    }
    return name;
}
