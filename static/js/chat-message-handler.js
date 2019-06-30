var socket = io();

socket.on('connect', function() {
  socket.emit('join', {});
});

var chat_input = document.getElementById("chat-input-textarea");
var chat_messages = document.getElementById("chat_messages");

var send_message = function(){
  msg = chat_input.value;
  msg = msg.trim()
  if (msg != ''){
    chat_input.value = null;
    socket.emit('message', msg);
  }
};

var render_message = function(msg){
  return "<div class='msg'><span class='msg-name'>" + msg.username + "</span><span class='msg-text'>" + msg.text + "</span></div><br>";
};

var render_sys_message = function(msg){
  return "<p class='sys-msg'>" + msg + "</p>"
};

socket.on("new message", function(msg){
  //msg --> chat-message
  console.log(msg.username + ": " + msg.text);
  chat_messages.innerHTML += render_message(msg);
  chat_messages.scrollTo(0,19000);
});

socket.on("new sys message", function(msg){
  //msg --> chat-message
  console.log("sys: " + msg);
  chat_messages.innerHTML += render_sys_message(msg);
  chat_messages.scrollTo(0,19000);
});

socket.on("not in chat", function(msg){
  console.log("sys: " + msg);
  leave();
});

var leave = function() {
  socket.emit('leave', {}, function() {
    socket.disconnect();
    // go back to the login page
    window.location.href = "logout";
  });
}
