// Initialize and add the map

async function initMap() {
  // The location of Uluru
  let map = new google.maps.Map(document.getElementById("map"),{
    center:{ lat: 10.315699, lng: 123.885437 },
    zoom:8,
  })


  const markers = [
    { lat: 10.315699, lng: 123.885437, info: "Seaweed"},
    { lat: 10.327970, lng: 123.941109, info: "Seagrass"},
    { lat: 10.315699, lng: 123.885437, info: "Coral"},
    
  ]

  markers.forEach(m=>{

    const marker = new google.maps.Marker({
      position: { lat: m.lat, lng: m.lng},
      title: "Seagrass",
    });

    const popupContent = new google.maps.InfoWindows()

    google.maps.event.addListener(marker, 'click',(function(marker){
      return function(){
        popupContent.setContent("m.info")
        popupContent.open(map, marker)
      }
  })

  // Request needed libraries.
  //@ts-ignore
  // const { Map } = await google.maps.importLibrary("maps");
  // const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // // The map, centered at Uluru
  // map = new Map(document.getElementById("map"), {
  //   zoom: 8,
  //   center: position,
  //   mapId: "DEMO_MAP_ID",
  // });

  // // The marker, positioned at Uluru
  // const marker = new AdvancedMarkerElement({
  //   map: map,
  //   position: position,
  //   title: "Seagrass",
  // });

  // const popupContent = new google.maps.InfoWindow()

  // google.maps.event.addListener(marker, 'cliick, (function(marker){
  //   return function(){
  //     popupContent.setContent("This is pop  up")
  //     popupContent.open(map, marker)
  //   }
  // })

})

initMap(map);