
function generateCoordinates() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

document.getElementById("coordinates").addEventListener("click", generateCoordinates);

function showPosition(position) {
    document.getElementById("latitude").value = position.coords.latitude.toFixed(6);
    document.getElementById("longitude").value = position.coords.longitude.toFixed(6);
}

// function setDefaultDateTime() {
//     var currentDateTime = new Date().toISOString();
//     document.getElementById("date_imported").value = currentDateTime.slice(0, 19);
// }


function setDefaultDateTime() {
    var currentDateTime = new Date().toISOString();
    var formattedDateTime = currentDateTime.slice(0, 16);
    document.getElementById("date_imported").value = formattedDateTime;
}



// document.addEventListener("DOMContentLoaded", function () {
//     // Wait for the DOM to be fully loaded before attaching event listeners
//     document.getElementById("coordinates").addEventListener("click", generateCoordinates);
//     setDefaultDateTime();
// });

// function generateCoordinates() {
//     if (navigator.permissions) {
//         navigator.permissions.query({ name: 'geolocation' }).then(permissionStatus => {
//             if (permissionStatus.state === 'granted') {
//                 navigator.geolocation.getCurrentPosition(showPosition, showError);
//             } else {
//                 alert('Location permission denied. Please enable location services.');
//             }
//         });
//     } else if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(showPosition, showError);
//     } else {
//         alert('Geolocation is not supported by this browser.');
//     }
// }

// function showPosition(position) {
//     console.log("Latitude:", position.coords.latitude.toFixed(6));
//     console.log("Longitude:", position.coords.longitude.toFixed(6));
    
//     // Update input values
//     document.getElementById("latitude").value = position.coords.latitude.toFixed(6);
//     document.getElementById("longitude").value = position.coords.longitude.toFixed(6);
// }

// function setDefaultDateTime() {
//     // Set default date and time
//     var currentDateTime = new Date().toISOString().slice(0, 16);
//     document.getElementById("date_imported").value = currentDateTime;
// }
