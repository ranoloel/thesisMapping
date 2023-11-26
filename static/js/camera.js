// function startCamera() {
//   const video = document.getElementById('videoElement');

//   navigator.mediaDevices.getUserMedia({ video: true })
//       .then((stream) => {
//           video.srcObject = stream;
//       })
//       .catch((error) => {
//           console.error('Error accessing camera:', error);
//           alert('Unable to access the camera. Please check permissions.');
//       });
// }

document.addEventListener('DOMContentLoaded', function () {
    // Get necessary elements
    const videoElement = document.getElementById('camera-view');
    const captureButton = document.getElementById('capture-btn');
    const cameraSelect = document.getElementById('camera-select');

    // Get user media with selected camera
    async function initializeCamera() {
        try {
            const constraints = {
                video: {
                    facingMode: cameraSelect.value, // Use selected camera
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            };
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            videoElement.srcObject = stream;
        } catch (error) {
            console.error('Error accessing camera:', error);
        }
    }

    // Switch camera when user selects a different option
    cameraSelect.addEventListener('change', initializeCamera);

    // Capture photo when the button is clicked
    captureButton.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        canvas.getContext('2d').drawImage(videoElement, 0, 0);
        
        //Now you can handle the captured image (e.g., send to server, display on page, etc.)
        const imageDataURL = canvas.toDataURL('image/png');
        console.log(imageDataURL);
    });

    // Initialize camera on page load
    initializeCamera();
});
