import socket from '../../socket';

const setUpSocket = (
  username,
  roomId,
  guesses,
  setGuesses,
  screenToDisplay,
  setScreenToDisplay,
) => {
  socket.on('connect', function() {
    console.log(`Websocket connected! Now joining room: ${roomId}`);
    socket.emit('join', {
      username,
      room: roomId,
    });
  });

  socket.on('receive_guess', function(guess) {
    console.log(`received guess: ${guess}`)
  });

  socket.on('disconnect', function() {
    console.log("websocket disconnected")
  });

  socket.on('receive_guess', function (data) {
    console.log(data);
    const newGuesses = [...guesses, {username: data.username, guess: data.guess}];
    setGuesses(newGuesses);
  });

  socket.on('receive_answer', function (data) {
    // console.log(data);
    // const newNode = document.createElement('div');
    // newNode.innerHTML = `<b>${data.username} guessed the word!</b>`;
    // document.getElementById('guesses').appendChild(newNode);
  });

  socket.on('new_player_join', function (data) {
    // console.log(data);
    // if (data.username !== "{{ username }}") {
    //     const newNode = document.createElement('div');
    //     newNode.innerHTML = `<b>${data.username}</b> has joined the room`;
    //     document.getElementById('guesses').appendChild(newNode);
    // }
  });

  socket.on('player_leave', function (data) {
    // console.log(data);
    // const newNode = document.createElement('div');
    // newNode.innerHTML = `<b>${data.username}</b> has left the room`;
    // document.getElementById('guesses').appendChild(newNode);
  });
}
export default setUpSocket;