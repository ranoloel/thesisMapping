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
            image.style.maxWidth = '100%'; // Set the maximum width of the image
            image.style.maxHeight = 'auto'; // Set the maximum height of the image for landscape display
            image.style.margin = '0 10px 10px 0'; // Adjust spacing as needed (top-right-bottom-left)

            removeButton.textContent = 'Remove';
            removeButton.onclick = function() {
                container.removeChild(imageContainer);
            };

            imageContainer.appendChild(image);
            imageContainer.appendChild(removeButton);
            container.appendChild(imageContainer);
        };

        reader.readAsDataURL(file);
    }
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
        window.location.href = '/train-img';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading images.');
    });
}