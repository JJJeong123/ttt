const videoElement = document.getElementById('input_video');



//==========================================
// 모델 로드 
const runHandpose = async() => {
  const model = await tf.loadLayersModel('http://127.0.0.1:8000/static/model/model.json ');
  console.log("Handpose model loaded");

  function onResults(results) {
    if (results.multiHandLandmarks) {
      for (const landmarks of results.multiHandLandmarks) {
        let prediction = model.predict(tf.tensor(pre_process_landmark(landmarks), [1, 42])); 
        let result = Math.max.apply(null, prediction.arraySync()[0]);
        if(result > 0.9 & result < 1){
          console.log(result);
          console.log(prediction.arraySync()[0].indexOf(result));
          return;
        }
      }
    }
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
  });
  
  camera.start();

  
}

runHandpose();
//==========================================



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


// 전처리 함수
function pre_process_landmark(landmark_list) {
    let temp_landmark = landmark_list;
    let landmark_array = new Array
  
    let base_x = 0;
    let base_y = 0;
    for (let i = 0; i < landmark_list.length; i++) {
      if (i === 0) base_x, base_y = landmark_list[i].x, landmark_list[i].y;
  
      temp_landmark[i].x = temp_landmark[i].x - base_x;
      temp_landmark[i].y = temp_landmark[i].y - base_y;
      landmark_array.push(temp_landmark[i].x);
      landmark_array.push(temp_landmark[i].y);
    }
  
    let max_value = -1;
    landmark_array.map((i) => {
      if (max_value < Math.abs(i)) {
        max_value = Math.abs(i);
      }
    });
  
    function normalize_(n) {
      return n / max_value
    }
    let result = landmark_array.map((i) => {
      return normalize_(i)
    })
    return result
  }
  