// Global array to keep track of files currently being displayed
let displayedFiles = [];

function displayImage() {
    const input = document.getElementById('imageInput');
    const container = document.getElementById('imageContainer');

    container.innerHTML = ''; // Clear previous images
    displayedFiles = []; // Reset the displayed files array

    for (const file of input.files) {
        displayedFiles.push(file); // Add file to the displayedFiles array

        const reader = new FileReader();
        reader.onload = function (e) {
            const imageContainer = document.createElement('div');
            imageContainer.style.border = '1px solid #ddd'; // Added border
            imageContainer.style.borderRadius = '4px'; // Rounded corners
            imageContainer.style.padding = '5px'; // Padding around the image
            imageContainer.style.margin = '10px'; // Margin around the container
            imageContainer.style.width = 'auto'; // Auto-width based on the content
            imageContainer.style.height = 'auto'; // Auto-height based on the content
            imageContainer.style.boxShadow = '0 4px 8px 0 rgba(0,0,0,0.2)'; // Shadow for depth
            imageContainer.style.textAlign = 'center'; // Center aligning the contents

            const image = new Image();
            image.src = e.target.result;
            image.style.width = '100%'; // Increased width
            image.style.height = 'auto'; // Height auto for aspect ratio
            image.style.marginBottom = '5px'; // Margin bottom for spacing

            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.className = 'btn btn-danger btn-sm';
            removeButton.style.marginTop = '5px'; // Adjusted margin top

            removeButton.onclick = function() {
                container.removeChild(imageContainer);
                const index = displayedFiles.indexOf(file);
                if (index > -1) {
                    displayedFiles.splice(index, 1);
                }
            };

            imageContainer.appendChild(image);
            imageContainer.appendChild(removeButton);
            container.appendChild(imageContainer);
        };

        reader.readAsDataURL(file);
    }
    container.style.display = 'flex';
    container.style.flexWrap = 'wrap';
    container.style.justifyContent = 'space-between';
}


function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

function submitImages() {
    openModal();
    if (displayedFiles.length === 0) {
        closeModal();
        alert('Please select at least one image before submitting.');
        return;
    }
    const formData = new FormData();
    for (const file of displayedFiles) {
        formData.append('images', file);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('imageContainer');
        container.innerHTML = '';
        window.location.href = '/detected-page-message';
    })
    .catch(error => {
        closeModal();
        console.error('Error:', error);
        alert('An error occurred while uploading images.');
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("coordinates").addEventListener("click", generateCoordinates);
});

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
