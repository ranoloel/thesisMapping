function displayImage() {
    const input = document.getElementById('imageInput');
    const container = document.getElementById('imageContainer');

    container.innerHTML = ''; // Clear previous images

    for (const file of input.files) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const imageContainer = document.createElement('div');
            const image = new Image();
            const removeButton = document.createElement('button');

            image.src = e.target.result;
            image.style.width = '100%'; // Set the width of the image
            image.style.height = 'auto'; // Set the height of the image for landscape display

            removeButton.textContent = 'X';
            // removeButton.innerHTML = '<i class="fas fa-times">x</i>'; // Using Font Awesome delete icon
            removeButton.className = 'btn btn-danger btn-sm'; // Bootstrap styling for the button
            removeButton.style.marginTop = '-45px'; // Set margin top
            removeButton.style.marginBottom = '5px'; // Set margin bottom
            removeButton.onclick = function() {
                container.removeChild(imageContainer);
            };

            imageContainer.appendChild(image);
            imageContainer.appendChild(removeButton);
            container.appendChild(imageContainer);
        };

        reader.readAsDataURL(file);
    }

    // Set container style for flex display
    container.style.display = 'flex';
    container.style.flexWrap = 'wrap';
    container.style.justifyContent = 'space-between'; // Adjust as needed for spacing
}



function submitImages() {
    const input = document.getElementById('imageInput');

    if (input.files.length === 0) {
        alert('Please select at least one image before submitting.');
        return;
    }

    const formData = new FormData();
    for (const file of input.files) {
        formData.append('images', file);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Optionally, clear the displayed images
        const container = document.getElementById('imageContainer');
        container.innerHTML = '';
        window.location.href = '/gallery-results';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading images.');
    });
}