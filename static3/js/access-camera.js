// script.js

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
  
    // Use navigator.mediaDevices.getUserMedia to access the camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        // Assign the camera stream to the video element
        video.srcObject = stream;
      })
      .catch((error) => {
        console.error('Error accessing camera:', error);
      });
  });

    // Function to preview the selected image
    function previewImage() {
      const input = document.getElementById('imageInput');
      const preview = document.getElementById('preview');

      // Check if a file is selected
      if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
          // Set the preview image source to the selected file
          preview.src = e.target.result;
        };

        // Read the selected file as a data URL
        reader.readAsDataURL(input.files[0]);
      }
    }

// Function to submit the image and data to the server

function submitImage() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];

  // Check if a file is selected
  if (file) {
    // Get the image date and ID (you can customize this part)
    const imageDate = new Date().toISOString();
    const imageId = generateImageId();

    // Create a FormData object and append the file, date, and ID
    const formData = new FormData();
    formData.append('file', file);
    formData.append('date', imageDate);
    formData.append('id', imageId);

    // Use fetch to send the FormData to the server
    fetch('/upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      console.log('Server response:', data);
      alert('Image uploaded successfully!');
    })
    .catch(error => {
      console.error('Error uploading image:', error);
      alert('Error uploading image. Please try again.');
    });
  } else {
    alert('Please select an image to upload.');
  }
}

// Function to generate a unique image ID (you can customize this part)
function generateImageId() {
  return 'img_' + Math.random().toString(36).substr(2, 9);
}