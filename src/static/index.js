function onLoad() {
	initializeSocket();
}

var websocket;
var targetUrl = 'ws://${location.host}/echo';

function initializeSocket() {
	console.log("opening socket");
	websocket = new WebSocket(targetUrl);
	websocket.onopen = onOpen;
	websocket.onclose = onClose;
	websocket.onmessage = onMessage;
}

function onOpen(event) {
	console.log("Open");
}

function onClose(event) {
	console.log("closing");
}

function onMessage(event) {
	console.log("Message: ",event);
}

function sendMessage(message) {
	websocket.sent(message);
}


function update(data) {
	console.log("update", data);
}


const log = (text, color) => {
	logtext_element=document.getElementById('log')
	logtext=logtext_element.innerHTML

	logtext_element.innerHTML = `<span style="color: ${color}">${text}</span><br>` + logtext;
};

const socket = new WebSocket('ws://' + location.host + '/echo');
socket.addEventListener('message', ev => {
	log('<<< ' + ev.data, 'blue');
});

socket.addEventListener('close', ev => {
	log('<<< closed');
});

document.getElementById('commandform').onsubmit = ev => {
	ev.preventDefault();
	const textField = document.getElementById('command');
	log('>>> ' + textField.value, 'red');
	socket.send(textField.value);
	textField.value = '';
};
