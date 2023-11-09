const videoElement = document.getElementById("video");
const canvasElement = document.getElementById("canvas");
const captureButton = document.getElementById("captureBtn");
const messageElement = document.getElementById("message");
const canvasContext = canvasElement.getContext("2d");

let greenBoxDetected = false;

navigator.mediaDevices.getUserMedia({ video: {} })
  .then(function (stream) {
    videoElement.srcObject = stream;
    videoElement.play();
  })
  .catch(function (err) {
    console.error("Error accessing the webcam: " + err);
  });

tracking.track('#video', new tracking.FaceTracker());

tracking.track('#video', new tracking.FaceTracker({ 
  onTrack: function(event) {
    canvasContext.clearRect(0, 0, canvasElement.width, canvasElement.height);

    if (event.data.length === 0) {
      greenBoxDetected = false;
      messageElement.textContent = "No face detected.";
    } else {
      greenBoxDetected = true;
      messageElement.textContent = "";
      event.data.forEach(function(rect) {
        canvasContext.strokeStyle = '#00FF00';
        canvasContext.strokeRect(rect.x, rect.y, rect.width, rect.height);
      });
    }
  }
}));

captureButton.addEventListener("click", function () {
  if (greenBoxDetected) {
    canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    const imageData = canvasElement.toDataURL("image/png");
    
    // Send imageData to a server endpoint using fetch API
    fetch("YOUR_SERVER_URL", {
      method: "POST",
      body: JSON.stringify({ image: imageData }),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      // Handle the response from the server
      console.log("Image sent successfully!");
    })
    .catch(error => {
      console.error("Error sending image: " + error);
    });
  } else {
    messageElement.textContent = "No face detected to capture.";
  }
});
