// -- Running Code
var agentsArray = [];
var neighborhoodsArray = [];
loadJSON(
    'data.json',
    (data) => { neighborhoodsArray = setup(data) },
    console.error
);


// -- Definition
function setup(neighborhoodData) {
    // TODO: Perform Setup Based on Data HERE
    console.log(neighborhoodData);
    return []
}

function loadJSON(path, success, error)
{
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200 && success) success(JSON.parse(xhr.responseText));
            else if (error) error(xhr);
        }
    };
    xhr.open("GET", path, true);
    xhr.send();
}

function Neighborhood(location, startingRent, housingUnits) {
    this.location = location; // in lat lon
    this.neighbors = [];
    this.rent = startingRent;
    this.agents = [];
    this.income = calcIncome(this);
    this.capacity = housingUnits;
    // this.name = function() {
    //     // if (this.neighborhood)
    //     return this.firstName + " " + this.lastName
    // }
}

function calcIncome(neighborhood)
{
  var sum = 0;
  for (var i = 0; i < neighborhood.agents.length; i++)
  {
    sum = sum + neighborhood.agents[i].salary;
  }
  neighborhood.income = sum / neighborhood.agents.length;
  return neighborhood.income;
}

function determineNeighbors(neighborhood)
{
  var closestNeighbor;
  var closestDist;
  for (var i = 0; i < neighborhoodsArray.length; i++)
  {
    distance = getDistance(neighborhood, neighborhoodsArray[i]);
    // update closest neighborhood
    if (distance < closestDist)
    {
      closestDist = distance;
      closestNeighbor = neighborhoodsArray[i];
    }
    // connect nodes that are within 900 meters with an edge
    if (distance < 900) // meters
    {
      neighborhood.neighbors.push(neighborhoodsArray[i]);
    }
  }
  // If it is not close enough to get connected,
  // just connect it to the closes neighbor
  if (neighborhood.neighbors.length == 0)
  {
    neighborhood.neighbors.push(closestNeighbor);
  }
}

// Calculate distance between two nodes
// using Mercator projection
function getDistance(neigh1, neigh2)
{
  var lat1 = neigh1.location[0];
  var lon1 = neigh1.location[1];
  var lat2 = neigh2.location[0];
  var lon2 = neigh2.location[1];

  var r = 6371000.0; // meters
  var phi1 = lat1*2*Math.PI/360.0; // convert to radians
  var phi2 = lat2*2*Math.PI/360.0; // convert to radians
  var deltaPhi = (lat2 - lat1)*2*Math.PI/360.0;
  var deltaLambda = (lon2 - lon1)*2*Math.PI/360.0;

  var a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

  var d = r * c;
  return d;
}

function Agent(startingNeighborhood, startingSalary) {
    this.neighborhood = startingNeighborhood;
    this.salary = startingSalary;
    startingNeighborhood.agents.push(this);
    // this.takeStep = function() {
    //     // if (this.neighborhood)
    //     return this.firstName + " " + this.lastName
    // };
}

function monthStep()
{
  neighborhoodsArray.sort(function (a, b) {
    if (a.rent > b.rent) {
      return 1;
    }
    if (a.rent < b.rent) {
      return -1;
    }
    // a must be equal to b
    return 0;
  });

  timeStep();
}


// Happens multiple times a month
function timeStep()
{
  // loop through neighborhoods
  for (var i = 0; i < neighborhoodsArray.length; i++)
  {
    agentsLoopOrder = shuffle(neighborhoodsArray[i].agents); // shuffle agents
    var deltaArray = [];
    //looping through all neighborhoods with lower rent
    for (var k = 0; k < i; k++)
    {
      //check if neighborhood has capacity
      if (neighborhoodsArray[k].agents.length < neighborhoodsArray[k].capacity)
      {
        //determine delta between rent and average income in neighborhood
        var delta = neighborhoodsArray[k].income - neighborhoodsArray[k].rent;
        //add neighborhood to list return ordered list of neighborhood sorted by deltas
        deltaArray.push([neighborhoodsArray[k], delta])
      }
    }

    //sort array of arrays by low-high delta
    deltaArray.sort(function(a, b) {
        if (a[1] < b[1]) return -1;
        if (a[1] > b[1]) return 1;
        return 0;
      });

    // Loop through agents
    for (var j = 0; j < agentsLoopOrder.length; j++)
    {
      potentialNeighborhoods = [];
      // check if needs to move
      // the neighborhood has gotten too expensive
      if (agentsLoopOrder[j].salary*0.45 >= neighLoopOrder[i].rent)
      {
        //loop through list of deltas - highest to lowest
        for (k = deltaArray.length -1; k >= 0; k-- ){
           //check that rent of neighborhood is less than 30% of income
          if (deltaArray[k][0].rent <= agentsLoopOrder[j].salary*.3){
            //and check that there is still space in neighborhood
            if (deltaArray[k][0].agents.length < deltaArray[k][0].capacity){
              potentialNeighborhoods.push(deltaArray[k][0]);
              //return list of 5 top options
              if (potentialNeighborhoods.length == 5){
                break;
              }
            }

          }
        }
      }
      // find place to move to (with pathplanning) on 5 top options
      var distance = Infinity;
      var closestNeighbor;
      for (var l = 0; l < potentialNeighborhoods.length; l++){
        if (findShortestPath(agentsLoopOrder[j].neighborhood, potentialNeighborhoods[l]) < distance){
          closestNeighbor = potentialNeighborhoods[l]
        }
      }
    }
  }

}


// Shuffle array by swapping elements
// http://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

//////////////////////////////////////////////////////////////////////////
//Shortest path algorithm 

// function findShortestPath(currentLocation, newLocation){
  
// }
