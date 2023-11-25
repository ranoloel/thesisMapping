let map;

function initializeMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 10.315699, lng: 123.885437 },
    zoom: 8,
  });

  // Fetch marker data from the API
  fetch('/fetch_markers')
    .then(response => response.json())
    .then(data => {
      const markers = data.markers;

      // Define custom icons for different marker types
      const iconMapping = {
        "seaweed": 'static/icon/seaweed.png',
        "seagrass": 'static/icon/seagrass.png',
        "coral": 'static/icon/coral.png',
        // Add more mappings as needed
      };

      markers.forEach((m) => {
        const customMarkerIcon = {
          url: iconMapping[m.class_type], // Select the appropriate icon based on m.class_type
          scaledSize: new google.maps.Size(32, 32),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(16, 32),
        };

        const marker = new google.maps.Marker({
          position: { lat: parseFloat(m.latitude), lng: parseFloat(m.longitude) },
          map: map,
          icon: customMarkerIcon,
        });

        const popupContent = new google.maps.InfoWindow();

        google.maps.event.addListener(marker, "click", (function (marker) {
          return function () {
            popupContent.setContent(m.class_type);
            popupContent.open(map, marker);
          };
        })(marker));
      });
    })
    .catch(error => {
      console.error("Error fetching marker data:", error);
    });
}

google.maps.event.addDomListener(window, "load", initializeMap);
