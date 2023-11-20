
let map;
    
function initializeMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 10.315699, lng: 123.885437 },
    zoom: 8,
  });

  const markers = [
    //Cebu Coordinates
    { lat: 10.315699, lng: 123.885437, info: "Seaweed" },
    { lat: 9.5167, lng: 123.4333, info: "Seagrass" },
    { lat: 9.9556609, lng: 123.4007598, info: "Coral" }
  ];

  // Define custom icons for different marker types
  const iconMapping = {
    "Seaweed": 'static/icon/seaweed.png', // Replace with the URL of the Seaweed icon
    "Seagrass": 'static/icon/seagrass.png', // Replace with the URL of the Seagrass icon
    "Coral": 'static/icon/coral.png', // Replace with the URL of the Coral icon test
  };

  markers.forEach((m) => {
    const customMarkerIcon = {
      url: iconMapping[m.info], // Select the appropriate icon based on m.info
      scaledSize: new google.maps.Size(32, 32),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(16, 32),
    };

    const marker = new google.maps.Marker({
      position: { lat: m.lat, lng: m.lng },
      map: map,
      icon: customMarkerIcon,
    });

    const popupContent = new google.maps.InfoWindow();

    google.maps.event.addListener(marker, "click", (function (marker) {
      return function () {
        popupContent.setContent(m.info);
        popupContent.open(map, marker);
      };
    })(marker));
  });
}
google.maps.event.addDomListener(window, "load", initializeMap);

//Get all the data using javascript - Not working atm
async function displayAllData() {
  try {
    const response = await fetch('/get_all_data');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Assuming there is a div with id 'dataContainer' in your HTML to display the data
    const dataContainer = document.getElementById('dataContainer');

    // Clear existing content in the container
    dataContainer.innerHTML = '';

    // Loop through the data and create HTML elements for each item
    data.forEach(item => {
      const listItem = document.createElement('li');
      listItem.textContent = `ID: ${item.id}, Image: ${item.image}, Date imported: ${item.date_imported}, Latitude: ${item.latitude}, Class Type: ${item.class_type}, status: ${item.status}`;
      
      // Append the list item to the container
      dataContainer.appendChild(listItem);
    });

  } catch (error) {
    console.error('Error fetching and displaying data:', error);
  }
}

// Call the function when needed
displayAllData();
