// https://google.github.io/mediapipe/solutions/hands.html

const videoElement = document.getElementById('input_video');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');


let localStream = new MediaStream();
const constraints = {
    'video': true,
    'audio': true
}
userMedia = navigator.mediaDevices.getUserMedia(constraints)
.then(stream => {
    localStream = stream;
    console.log('Got MediaStream:', stream);
    var mediaTracks = stream.getTracks();
    for(i=0; i < mediaTracks.length; i++){
        console.log(mediaTracks[i]);
    }
    videoElement.srcObject = localStream;
    videoElement.muted = true;
    window.stream = stream; 
    audioTracks = stream.getAudioTracks();
    videoTracks = stream.getVideoTracks();
    audioTracks[0].enabled = true;
    videoTracks[0].enabled = true;
})
.catch(error => {
    console.error('Error accessing media devices.', error);
});


function onResults(results) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                     {color: '#00FF00', lineWidth: 5});
      drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
    }
  }
  canvasCtx.restore();
}

const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
  maxNumHands: 2,
  modelComplexity: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
hands.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await hands.send({image: videoElement});
  },
  width: 1280,
  height: 720
});
camera.start();