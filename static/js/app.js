
function optionChanged(selectedId) {
  console.log(selectedId);
  displayCharts(selectedId);
  //Because we do not have access to data we need to fetch it again
  //Anything we do with the data needs to be inside this promise
}

function displayCharts(song) {
  console.log(song);
 // Fetch data:
 d3.json("api/music").then((data) => {
  console.log(data)
 
    $('#example').DataTable( {
      destroy:true,
      data: data['table'],
      columns: [
          { title: "Track" },
          { title: "Streams" },
          { title: "Danceability" },
          { title: "Energy" },
          { title: "Acousticness" },
          { title: "Spotify" },
          { title: "Apple" },
          { title: "Artist" },
      ]
      } );
      
    
      
      //Everything with data has to be set in here
      let samples = data.table;
      console.log(samples);
      // Filter the data to get the values for the selected ID
      function selectArrayByColumn(samples, columnIndex, song) {
          return samples.find(arr => arr[columnIndex] === song);
      }
      var columnIndex = 0; // Column index to search (0-indexed)
      //var selectedSong = selectedId; // Value to search for
      var selectedArray = selectArrayByColumn(samples, columnIndex, song);
      console.log(selectedArray)
      danceability = selectedArray[2];
      energy = selectedArray[3];
      acousticness = selectedArray[4];
      spotify = selectedArray[5];
      apple = selectedArray[6];
      artist = selectedArray[7];


      console.log(danceability);

      //Do pie chart
      var data = [{
          values: [danceability,energy,acousticness],
          labels: ['Danceability', 'Energy', 'Acousticness'],
          type: 'pie'
          }];
          var layout = {
          height: 400,
          width: 500,
          title: 'Song Balance'
          };
      Plotly.newPlot('bubble', data, layout);

    //Do pie chart for artist
        //Is the artist more popular on Apply or Spotify?
        var trace1 = [{
          values: [spotify, apple],
          labels: ['Spotify', 'Apple'],
          type: 'pie'
          }];
          var layout1 = {
          height: 400,
          width: 500,
          title: 'How does popularity on Spotify compare to Apple?'
          };
      Plotly.newPlot("bar", trace1, layout1);

  })
}






$(document).ready(function() {



function init () {
  d3.json("api/music").then((data) => {
      console.log(data)
      // $(document).ready(function() {
        $('#example').DataTable( {
          data: data['table'],
          columns: [
              { title: "Track" },
              { title: "Streams" },
              { title: "Danceability" },
              { title: "Energy" },
              { title: "Acousticness" },
              {title: "Spotify"},
              {title: "Apple"},
              {title: "Artist"}
          ]
          } );
          //Everything with data has to be set in here
          let samples = data.table;
      //Define songs as a variable from table
function getFirstColumn(table) {
  var firstColumn = [];
  for (var i = 0; i < table.length; i++) {
    if (table[i].length > 0) {
      firstColumn.push(table[i][0]);
    } else {
      firstColumn.push(null); // If first column is missing, push null
    }
  }
  return firstColumn;
}
// Logs the songs to console
var songs = getFirstColumn(samples);
console.log(songs);
      // Fill the dropdown menu with all the songs
      let dropdownMenu = d3.select("#selDataset");
      for (let i=0; i<samples.length; i++) {
          dropdownMenu.append("option").text(songs[i]).property("value", songs[i]);
      }
      first = songs[0];
      //Display the charts and panel with the first ID
      displayCharts(first);
  });
}

init()

})

 
