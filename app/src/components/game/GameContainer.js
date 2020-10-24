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
import StartGame from './screens/StartGame';
import GamePlay from './GamePlay';
import GlobalContext from '../../context';

const GAME_END  = 'game_end';
const TIME_UP   = 'time up';
const NO_MODAL  = 'none';
const GAME_START  = 'game_start';
const CHOOSE_WORD = "choose_word"

function GameContainer(props) {
  console.log('running game container')
  const [socket, setSocket] = React.useState(socketIOClient(ENDPOINTS.root));
  const [gameStart, setGameStart] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);
  const [guesses, setGuesses] = React.useState([]);

  var global_choices = []

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
      console.log("done")
    });
  
    socket.on('receive_guess', function(guess) {
      console.log(`received guess: ${guess}`)
    });
  
    socket.on('disconnect', function() {
      console.log("websocket disconnected")
    });
  
    socket.on('receive_guess', function (data) {
      console.log(data);
      // const newGuesses = [...guesses, {username: data.username, guess: data.guess}];
      guesses.push(data.guess)
      const newGuesses = guesses 
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

    socket.on('new_game', function (data) {
      console.log(data);
      setModalToDisplay(GAME_START)

      socket.emit('start', {
        username,
        roomId,
      });
      
    });

    socket.on('end_game', function (data) {
      console.log("end game client")
      console.log(data);
      setModalToDisplay(GAME_END)
      
    });

    socket.on('choose_word', function (data) {
      console.log('Choosing Word');
      global_choices = data.options
      setModalToDisplay(CHOOSE_WORD)
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
      case GAME_START:
        return <StartGame />;
      case CHOOSE_WORD:
        return <div id="choices">{global_choices}</div>;
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