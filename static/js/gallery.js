
function generateCoordinates() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    document.getElementById("latitude").value = position.coords.latitude.toFixed(6);
    document.getElementById("longitude").value = position.coords.longitude.toFixed(6);
}

function setDefaultDateTime() {
    var currentDateTime = new Date().toISOString().slice(0, 16);
    document.getElementById("date_imported").value = currentDateTime;
}
