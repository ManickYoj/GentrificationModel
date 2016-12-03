var agentsArray = [];
var neighborhoodsArray = [];

function Neighborhood(location, startingRent) {
    this.location = location; // in lat lon
    this.neighbors = [];
    this.rent = startingRent;
    this.agents = [];
    this.income = calcIncome(this);
    this.name = function() {
        // if (this.neighborhood)
        return this.firstName + " " + this.lastName
    }
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

// function timeStep()
// {
//   neighLoopOrder = shuffle(neighborhoodsArray);
//   // loop through neighborhoods
//   for (var i = 0; i < neighLoopOrder.length; i++)
//   {
//     agentsLoopOrder = shuffle(neighLoopOrder[i].agents); // shuffle agents
//     // Loop through agents
//     for (var j = 0; j < agentsLoopOrder.length; j++)
//     {
//       // check if needs to move
//       if (agentsLoopOrder[j].salary >= )
//       // if needs to move
//         // find place to move to (with pathplanning)
//     }
//   }
//
// }

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

// var myFather = new Person("John", "Doe", 50, "blue");
// document.getElementById("demo").innerHTML =
// "My father is " + myFather.name();
