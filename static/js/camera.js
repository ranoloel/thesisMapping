 // Function to handle camera access
 async function startCamera() {
    try {
      // Get user media based on device type
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
      });

      // Display the video feed on the video element
      const videoElement = document.getElementById('cameraFeed');
      videoElement.srcObject = stream;

    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  }

  // Check if the device is a mobile phone
  function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }

  // Add click event listener to the camera button
  const cameraButton = document.getElementById('cameraButton');
  cameraButton.addEventListener('click', () => {
    // Start the camera based on device type
    if (isMobile()) {
      // If using a mobile phone, start camera access on button click
      startCamera();
    } else {
      // If using a laptop/desktop, start camera access immediately
      startCamera();
    }
  });
                                 