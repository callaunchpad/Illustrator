import React from 'react';
import GlobalContext from '../../context';
import Canvas from './canvas/Canvas';
// import socket from '../../socket';
export default function GamePlay(props) {
  const [guess, setGuess] = React.useState('');
  const globalContext = React.useContext(GlobalContext);
  const { username, roomId } = globalContext;
  const sendGuess = (e) => {
    // props.setMessages(props.messages.concat("hello"));
    // console.log('messages: ', props.messages);
    e.preventDefault();
    let g = guess.trim();
    if (g.length) {
      props.socket.emit('send_guess', {
        username,
        roomId,
        guess: g
      });
    }
  }
  const startGame = (e) => {
    e.preventDefault();
    props.socket.emit('start_game', {
        username,
        roomId: roomId
    });
  }
  return (
    <div className='gameplay container'>
      <form onSubmit={sendGuess}>
        <input
          type="text"
          id="guess_input"
          placeholder="Enter your guess here"
          value={guess}
          onChange={(e) => setGuess(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      <form onSubmit={startGame}>
        <button type="submit">Start Game</button>
      </form>
      <Canvas
        socket={props.socket}
        messages={props.messages}
      />
    </div>
  )
}
