/**
 * A container component that displays different screens
 * depending on the game state. All client socket logic is here.
 * By the time this component is displayed, the client should have already
 * joined a room and should already have a username
 */

import React from 'react'
import Modal from '@material-ui/core/Modal';
import { withRouter } from 'react-router-dom';
import socketIOClient from "socket.io-client";

import ENDPOINTS from '../../endpoints';
import End from './screens/End';
// import socket from '../../socket';
import Lobby from './Lobby';
import TimesUp from './screens/TimesUp';
import GamePlay from './GamePlay';
import GlobalContext from '../../context';

const GAME_END  = 'game_end';
const TIME_UP   = 'time up';
const NO_MODAL  = 'none';

function GameContainer(props) {
  console.log('running game container')
  const [socket, setSocket] = React.useState(socketIOClient(ENDPOINTS.root));
  const [gameStart, setGameStart] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);
  const [guesses, setGuesses] = React.useState([]);

  const globalContext = React.useContext(GlobalContext);
  // console.log(props.location.state.roomId);

  // redirect to home page is user or room id does not exist
  // this will typically happen if the user refreshes
  // can make this more robust laster by storing username, roomid in localstorage
  const { username, roomId } = globalContext;
  if (username === undefined || username.length === 0 || roomId === undefined || roomId.length === 0) {
    props.history.push("/");
  }

  React.useEffect(() => {
    setGameStart(true);
    console.log("using effect....");
    socket.on('connect', function() {
      console.log(`Websocket connected! Now joining room: ${roomId}`);
      socket.emit('join', {
        username,
        roomId,
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
      console.log(data);
      // const newNode = document.createElement('div');
      // newNode.innerHTML = `<b>${data.username} guessed the word!</b>`;
      // document.getElementById('guesses').appendChild(newNode);
    });
  
    socket.on('new_player_join', function (data) {
      console.log(data);
      // if (data.username !== "{{ username }}") {
      //     const newNode = document.createElement('div');
      //     newNode.innerHTML = `<b>${data.username}</b> has joined the room`;
      //     document.getElementById('guesses').appendChild(newNode);
      // }
    });
  
    socket.on('player_leave', function (data) {
      console.log(data);
      // const newNode = document.createElement('div');
      // newNode.innerHTML = `<b>${data.username}</b> has left the room`;
      // document.getElementById('guesses').appendChild(newNode);
    });

    // disconnect the socket when component unmounts
    return () => socket.disconnect();
  }, []);

  const displayScreen = () => {
    if (gameStart) {
      return <GamePlay socket={socket} guesses={guesses}/>;
    }
    return <Lobby />;
  }

  const displayModalContent = () => {
    switch(modalToDisplay) {
      case NO_MODAL:
        return null;
      case GAME_END:
        return <End />;
      case TIME_UP:
        return <TimesUp />;
      default:
        return (<span>Something's wrong with the screen display logic :(</span>);
    }
  }
  return (
    <div className='game container'>
      { displayScreen() }
      <Modal
        open={modalToDisplay !== NO_MODAL}
        onClose={() => setModalToDisplay(NO_MODAL)}
      >
        <div>
          <h1 style={{color: 'white'}}>{modalToDisplay}</h1>
          {displayModalContent()}
        </div>
      </Modal>
    </div>
  )
}
export default withRouter(GameContainer);