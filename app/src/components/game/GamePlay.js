import React from 'react';
import GlobalContext from '../../context';
import Canvas from './canvas/Canvas';
// import socket from '../../socket';
export default function GamePlay(props) {
  const [guess, setGuess] = React.useState('');
  const globalContext = React.useContext(GlobalContext);
  const { username, roomId } = globalContext;
  const sendGuess = (e) => {
    e.preventDefault();
    let guess = guess.trim();
    if (guess.length) {
      props.socket.emit('send_guess', {
        username,
        room: roomId,
        guess: guess
      });
    }
  }
  return (
    <div className='gameplay container'>
      <ul id="guesses">
        {props.guesses}
      </ul>
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
      <Canvas socket={props.socket}/>
    </div>
  )
}
