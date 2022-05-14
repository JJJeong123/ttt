// map peer usernames to corresponding RTCPeerConnections
let mapPeers = {};

//Get video properties
const localVideo = document.getElementById('localVideo');
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
    
    localVideo.srcObject = localStream;
    localVideo.muted = true;
    
    window.stream = stream; // make variable available to browser console

    audioTracks = stream.getAudioTracks();
    videoTracks = stream.getVideoTracks();

    // unmute audio and video by default
    audioTracks[0].enabled = true;
    videoTracks[0].enabled = true;
})
.catch(error => {
    console.error('Error accessing media devices.', error);
});


const runHandpose = async() => {
    const model = await handpose.load();
    console.log("Handpose model loaded");
   
    //Loop and detect hands
    let detectTimer = setInterval(() => {
        detect(model, detectTimer);
    }, 10);
}


const detect = async (model, detectTimer) => {
    //Make detections
    const hand = await model.estimateHands(localVideo);
    //console.log(hand);

    if (hand.length > 0) {
        const GE = new fp.GestureEstimator([
            fp.Gestures.VictoryGesture,
            fp.Gestures.ThumbsUpGesture,
        ]);
        const gesture = await GE.estimate(hand[0].landmarks, 4);
        if (gesture.gestures !== undefined && gesture.gestures.length > 0) {

            const confidence = gesture.gestures.map(
                (prediction) => prediction.confidence
            );
            
            const maxConfidence = confidence.indexOf(
                Math.max.apply(null, confidence)
            );

            let result = gesture.gestures.reduce((p, c) => { 
                return (p.score > c.score) ? p : c;
            });
            if (result.name ==='victory' && result.score > 9) {
                testfunction(result);
                clearInterval(detectTimer);
            }
        }
    }
}


function testfunction(result){
    console.log('result: ', result);
    alert(result.name);

    sendSignal('start-bargain', {});
}


// text messages
const messageInput = document.getElementById('message-input');
const btnSendMsg = document.getElementById('message-submit');
const ul = document.getElementById("message-log");

const loc = window.location;
let endPoint = '';

// web protocol -> http or https
let wsStart = 'ws://';
if(loc.protocol == 'https:'){
    wsStart = 'wss://';
}

// get shop id
let shopId = document.getElementById('shopId').textContent;
console.log('shopId:', shopId);
let roomName = shopId;

endPoint = wsStart + "127.0.0.1:8000" + '/ws/chat/' + roomName + '/';
console.log('EndPoint: ', endPoint);

let webSocket;

// get username
let username = document.getElementById('username').textContent;
console.log('Username: ',username);

const btnJoin = document.getElementById('startButton');
const btnHangup = document.getElementById('hangupButton');

// join room (initiate websocket connection)
btnJoin.onclick = () => {
    // disable and vanish join button
    btnJoin.disabled = true;
    btnJoin.style.visibility = 'hidden';

    webSocket = new WebSocket(endPoint);

    webSocket.onopen = function(e){
        console.log('Connection opened! ', e);
        sendSignal('new-peer', {});
    }
    
    // if message received
    webSocket.onmessage = webSocketOnMessage;
    
    webSocket.onclose = function(e){
        console.log('Connection closed! ', e);
    }
    
    webSocket.onerror = function(e){
        console.log('Error occured! ', e);
    }

    $("#productList").show();

    // shows products of the shop
    let table_products = $('#dataTableHover-prolist').DataTable({
        destroy: true,
        autoWidth: false,
        searching: false,
        paging: false,
    
        ajax: {
          'type' : 'GET',
          'url': '/chat/product-list?shopId=' + shopId,
          'dataSrc': 'products'
        },
        createdRow: function( row, data, dataIndex ) {
            $(row).on('click', function(e) {
                startAsk(data.name, data.id);
            });
          },
        columns: [
          {data : 'name'},
          {data : 'price'},
          {data : 'description'},
        ],
    });

    btnSendMsg.disabled = false;
    messageInput.disabled = false;
}

btnHangup.onclick = () => {
    btnJoin.disabled = false;
    btnJoin.style.visibility = 'show';
    btnSendMsg.disabled = true;
    messageInput.disabled = true;

    webSocket.close()
    
    webSocket.onclose = function(e){
        alert("통화가 종료되었습니다");
        console.log('Connection closed! ', e);
    }

    //use replace instead of href
    location.replace('/');
}


function webSocketOnMessage(event){
    var parsedData = JSON.parse(event.data);

    var action = parsedData['action'];
    // username of other peer
    var peerUsername = parsedData['peer'];
    
    console.log('action: ', action);
    console.log('peerUsername: ', peerUsername);

    if(peerUsername == username){
        // ignore all messages from oneself
        return;
    }
    
    // channel name of the sender of this message
    // used to send messages back to that sender
    // hence, receiver_channel_name
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];
    console.log('receiver_channel_name: ', receiver_channel_name);


    /*
    if action is 'new-peer'
    (커넥션이 만들어지는 순간 (onopen) new-peer 액션인 메세지 send 됨)
    */ 
    if(action === 'new-peer'){
        console.log('New peer: ', peerUsername);
        // create new RTCPeerConnection

        createOfferer(peerUsername, receiver_channel_name);
        return;
    }

    if(action === 'new-offer'){
        console.log('Got new offer from ', peerUsername);

        // create new RTCPeerConnection
        // set offer as remote description
        var offer = parsedData['message']['sdp'];
        console.log('Offer: ', offer);
        var peer = createAnswerer(offer, peerUsername, receiver_channel_name);

        return;
    }
    

    if(action === 'new-answer'){
        // get the corresponding RTCPeerConnection
        var peer = null;
        peer = mapPeers[peerUsername][0];

        // get the answer
        var answer = parsedData['message']['sdp'];
        
        console.log('mapPeers:');

        for(key in mapPeers){
            console.log(key, ': ', mapPeers[key]);
        }

        console.log('peer: ', peer);
        console.log('answer: ', answer);

        // set remote description of the RTCPeerConnection
        peer.setRemoteDescription(answer);

        return;
    }

    if(action === 'end-bargain'){
        var bargainResult = parsedData['message']['bargain_result'];
        console.log('흥정 종료 결과: ' + bargainResult);

        if(bargainResult === 'Accepted' ){
            alert("쿠폰이 발급되었습니다.");
        }else{
            alert("흥정이 거절되었습니다");
        }
        
        return;
    }
}

messageInput.addEventListener('keyup', function(event){
    if(event.keyCode == 13){
        event.preventDefault();

        // click send text message button
        btnSendMsg.click();
    }
});

btnSendMsg.onclick = btnSendMsgOnClick;

function btnSendMsgOnClick(){
    var message = messageInput.value;
    
    var li = document.createElement("li");
    li.appendChild(document.createTextNode("Me: " + message));
    ul.appendChild(li);
    
    var dataChannels = getDataChannels();

    console.log('Sending: ', message);

    // send to all data channels
    for(index in dataChannels){
        dataChannels[index].send(username + ': ' + message);
    }
    
    messageInput.value = '';
}


function sendSignal(action, message){
    webSocket.send(
        JSON.stringify(
            {
                'peer': username,
                'action': action,
                'message': message,
            }
        )
    )
}

function createOfferer(peerUsername, receiver_channel_name){
  
    var peer = new RTCPeerConnection(null);
    
    // add local user media stream tracks
    addLocalTracks(peer);

    // create and manage an RTCDataChannel
    var dc = peer.createDataChannel("channel");
    dc.onopen = () => {
        console.log("Connection opened.");
    };
    var remoteVideo = null;
    // none of the peers are sharing screen (normal operation)

    dc.onmessage = dcOnMessage;

    remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);
    console.log('Remote video source: ', remoteVideo.srcObject);

    // store the RTCPeerConnection
    // and the corresponding RTCDataChannel
    mapPeers[peerUsername] = [peer, dc];

    peer.oniceconnectionstatechange = () => {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
            console.log('Deleting peer');
            delete mapPeers[peerUsername];
            if(iceConnectionState != 'closed'){
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    };

    peer.onicecandidate = (event) => {
        if(event.candidate){
            console.log("New Ice Candidate! Reprinting SDP" + JSON.stringify(peer.localDescription));
            return;
        }
        
        // event.candidate == null indicates that gathering is complete
        
        console.log('Gathering finished! Sending offer SDP to ', peerUsername, '.');
        console.log('receiverChannelName: ', receiver_channel_name);

        // send offer to new peer
        // after ice candidate gathering is complete
        sendSignal('new-offer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name,
        });
    }


    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(function(event){
            console.log("Local Description Set successfully.");
        });

    console.log('mapPeers[', peerUsername, ']: ', mapPeers[peerUsername]);

    return peer;
}

// create RTCPeerConnection as answerer

function createAnswerer(offer, peerUsername, receiver_channel_name){
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    // if none are sharing screens (normal operation)

    // set remote video
    var remoteVideo = createVideo(peerUsername);

    // and add tracks to remote video
    setOnTrack(peer, remoteVideo);

    // it will have an RTCDataChannel
    peer.ondatachannel = e => {
        console.log('e.channel.label: ', e.channel.label);
        peer.dc = e.channel;
        peer.dc.onmessage = dcOnMessage;
        peer.dc.onopen = () => {
            console.log("Connection opened.");
        }

      
        mapPeers[peerUsername] = [peer, peer.dc];
    }

    peer.oniceconnectionstatechange = () => {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
            delete mapPeers[peerUsername];
            if(iceConnectionState != 'closed'){
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    };

    peer.onicecandidate = (event) => {
        if(event.candidate){
            console.log("New Ice Candidate! Reprinting SDP" + JSON.stringify(peer.localDescription));
            return;
        }
        
        // event.candidate == null indicates that gathering is complete

        console.log('Gathering finished! Sending answer SDP to ', peerUsername, '.');
        console.log('receiverChannelName: ', receiver_channel_name);

    
        sendSignal('new-answer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name,
        });
    }

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log('Set offer from %s.', peerUsername);
            return peer.createAnswer();
        })
        .then(a => {
            console.log('Setting local answer for %s.', peerUsername);
            return peer.setLocalDescription(a);
        })
        .then(() => {
            console.log('Answer created for %s.', peerUsername);
            console.log('localDescription: ', peer.localDescription);
            console.log('remoteDescription: ', peer.remoteDescription);
        })
        .catch(error => {
            console.log('Error creating answer for %s.', peerUsername);
            console.log(error);
        });

    return peer
}

function dcOnMessage(event){
    var message = event.data;
    
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(message));
    ul.appendChild(li);
}

// get all stored data channels
function getDataChannels(){
    var dataChannels = [];
    
    for(peerUsername in mapPeers){
        console.log('mapPeers[', peerUsername, ']: ', mapPeers[peerUsername]);
        var dataChannel = mapPeers[peerUsername][1];
        console.log('dataChannel: ', dataChannel);

        dataChannels.push(dataChannel);
    }

    return dataChannels;
}

// get all stored RTCPeerConnections
// peerStorageObj is an object (either mapPeers or mapScreenPeers)
function getPeers(peerStorageObj){
    var peers = [];
    
    for(peerUsername in peerStorageObj){
        var peer = peerStorageObj[peerUsername][0];
        console.log('peer: ', peer);

        peers.push(peer);
    }

    return peers;
}

// for every new peer
// create a new video element
function createVideo(peerUsername){
    var remoteVideo = document.getElementById('remoteVideo');

    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsinline = true;



    return remoteVideo;
}

// set onTrack for RTCPeerConnection
function setOnTrack(peer, remoteVideo){
    console.log('Setting ontrack:');
    // create new MediaStream for remote tracks
    var remoteStream = new MediaStream();

    // assign remoteStream as the source for remoteVideo
    remoteVideo.srcObject = remoteStream;

    console.log('remoteVideo: ', remoteVideo.id);

    peer.addEventListener('track', async (event) => {
        console.log('Adding track: ', event.track);
        remoteStream.addTrack(event.track, remoteStream);
    });
}


function addLocalTracks(peer){
    // add user media tracks
    localStream.getTracks().forEach(track => {
        console.log('Adding localStream tracks.');
        peer.addTrack(track, localStream);
    });

    return;
}

function removeVideo(video){
    // get the video wrapper
    var videoWrapper = video.parentNode;
    // remove it
    videoWrapper.parentNode.removeChild(videoWrapper);
}


function startAsk(productName, productId){
    console.log("startAsk");
    console.log('Selected product name: ', productName);
    console.log('Selected product id: ', productId);

    $('#message-input').val('사장님, ' +productName + ' 상품 보여주세요!'); 
    btnSendMsg.click();
    sendSignal('new-product', {
        'selected_product': productId,
        'selected_product_name': productName,
    });
    $('#selectedPro').val(productName); 

    runHandpose();
}



/*
if productName
victory => chat 
thumbs up => yes
thumbs down => no

if yes => database order
*/