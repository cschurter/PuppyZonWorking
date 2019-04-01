// // Creating our initial map object
// // We set the longitude, latitude, and the starting zoom level
// // This gets inserted into the div with an id of 'map'
// var myMap = L.map('map', {
//     center: [45.52, -122.67],
//     zoom: 13
//   });

//   // Adding a tile layer (the background map image) to our map
//   // We use the addTo method to add objects to our map
//   L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
//     attribution: 'Map data &copy; <a href=\'https://www.openstreetmap.org/\'>OpenStreetMap</a> contributors, <a href=\'https://creativecommons.org/licenses/by-sa/2.0/\'>CC-BY-SA</a>, Imagery © <a href=\'https://www.mapbox.com/\'>Mapbox</a>',
//     maxZoom: 18,
//     id: 'mapbox.streets',
//     accessToken: API_KEY
//   }).addTo(myMap);

//Get data to be displayed in the table
// const url = `listings`;
// console.log('URL = ', url);


d3.json(url).then(function (data) {
  // console.log(data);

  var mapdata = [];
  //Add row elements
  data.forEach((pet) => {
    var dt = {};
    var marker = {
      size: 14
    };

    dt['type'] = 'scattermapbox';
    dt['lat'] = [pet['Lat']];
    dt['lon'] = [pet['Lng']];

    dt['mode'] = 'markers';
    dt['marker'] = marker;
    dt['text'] = [pet['primary breed']];

    mapdata.push(dt);
  });
  console.log('Mapdata printed below');
  console.log(mapdata);

  // //coupled hover event - show grouped categories
  // var mapdata = [{
  //   type: 'scattermapbox',
  //   lat: ['45.5017'],
  //   lon: ['-73.5673'],
  //   mode: 'markers',
  //   marker: {
  //     size: 14
  //   },
  //   text: ['Montreal']
  // }, {
  //   type: 'scattermapbox',
  //   lat: ['46.5017'],
  //   lon: ['-72.5673'],
  //   mode: 'markers',
  //   marker: {
  //     size: 14
  //   },
  //   text: ['Not Montreal']
  // }]

  var layout = {
    autosize: true,
    hovermode: 'closest',
    mapbox: {
      bearing: 0,
      center: {
        lat: 41,
        lon: -88
      },
      pitch: 0,
      zoom: 4
    },
    showlegend: false
  }

  Plotly.setPlotConfig({
    mapboxAccessToken: API_KEY
  })

  Plotly.plot('map', mapdata, layout)



});
