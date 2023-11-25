function startCamera() {
  const video = document.getElementById('videoElement');

  navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
          video.srcObject = stream;
      })
      .catch((error) => {
          console.error('Error accessing camera:', error);
          alert('Unable to access the camera. Please check permissions.');
      });
}