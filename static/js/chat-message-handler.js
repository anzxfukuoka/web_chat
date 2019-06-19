alert( document.cookie );

var socket = io();
socket.on('connect', function() {
  socket.emit('message', {username: "kami♥", text: 'I\'m connected!'});
});

var chat_input = document.getElementById("chat-input-textarea");

var send_message = function(){
  msg = chat_input.value;

  chat_input.value = null;

  socket.emit('message', {username: "kami♥", text: msg});
};

socket.on("new message", function(json){
  console.log(json.text);
});
