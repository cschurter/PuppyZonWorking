// Creating our initial map object
// We set the longitude, latitude, and the starting zoom level
// This gets inserted into the div with an id of 'map'

var buttonClickedTimes = 0;
var myMap;

var findPetButton = d3.select("#FindPet");
// Creating our initial map object
// We set the longitude, latitude, and the starting zoom level
// This gets inserted into the div with an id of 'map'
// var myMap = L.map("mapid", {
//   center: [45.52, -122.67],
//   zoom: 13
// });


// L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
//   attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//   maxZoom: 18,
//   id: 'mapbox.streets',
//   accessToken: API_KEY
// }).addTo(myMap);


//on Button click event
findPetButton.on("click", function () {
  buttonClickedTimes = buttonClickedTimes + 1;

  // var myMap = L.map("mapid", {
  //   center: [45.52, -122.67],
  //   zoom: 5
  // });
  
  // L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  //   attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  //   maxZoom: 18,
  //   id: "mapbox.streets",
  //   accessToken: API_KEY
  // }).addTo(myMap);



  if (buttonClickedTimes > 1) {
    console.log("button clicked times ", buttonClickedTimes);
    //clear the map
    // myMap.off();
    // myMap.remove();

    //refresh table
    tbody.html(' ');

  }

  //Filter  on zipcode
  var zipcode_value = zipcode.property("value");



  d3.json(url).then(function (data) {

    var listResults = [];

    //filter and package results
    data.forEach(pet => {
      if (pet["postcode"] == zipcode_value) {
        listResults.push(pet);

        populateTable(pet);

      }

    });


    myMap = L.map("mapid", {
      //center: [data[0]['Lat'], data[0]['Lng']],
      center: [listResults[0]['Lat'], listResults[0]['Lng']],
      zoom: 5
    });

    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.streets",
      accessToken: API_KEY
    }).addTo(myMap);


    //add markers for each pet location
    listResults.forEach(pet => {
      L.marker([pet['Lat'], pet['Lng']])
        .bindPopup("<h4>Breed: </h4>" + pet["primary breed"] + "<br> <h4>Gender: </h4>" + pet["gender"] + "<br> <h4>Age: </h4>" + pet["age"] + "<br> <h4>zipcode: </h4>" + pet["postcode"])
        .addTo(myMap);
    });




  });


});

