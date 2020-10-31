/**
 * A container component that displays different screens
 * depending on the game state. All client socket logic is here.
 * By the time this component is displayed, the client should have already
 * joined a room and should already have a username
 */

import React from 'react'
// import Modal from '@material-ui/core/Modal';
import { withRouter } from 'react-router-dom';
import socketIOClient from "socket.io-client";
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';

import ENDPOINTS from '../../endpoints';
import End from './screens/End';
// import socket from '../../socket';
import Lobby from './Lobby';
import TimesUp from './screens/TimesUp';
import StartGame from './screens/StartGame';
import GamePlay from './GamePlay';
import GlobalContext from '../../context';
import { CardActionArea } from '@material-ui/core';
import ChooseWord from './screens/ChooseWord';

const GAME_END  = 'game_end';
const TIME_UP   = 'time up';
const NO_MODAL  = 'none';
const GAME_START  = 'game_start';
const CHOOSE_WORD = "Pick a word!"

function GameContainer(props) {
  const [socket, _] = React.useState(socketIOClient(ENDPOINTS.root));
  const [gameStart, setGameStart] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);

  const [messages, setMessages] = React.useState([]); // list of strings that are displayed in the canvas chat
  const [players, setPlayers]   = React.useState([]); // list of players that joined
  const [guesses, setGuesses]   = React.useState([]); // list of player names and their guesses
  const [answered, setAnswered] = React.useState([]); // list of players that guessed the word
  const [wordChoices, setWordChoices] = React.useState([]); // list of word choices to be displayed

  const messagesRef    = React.useRef(messages);
  const playersRef     = React.useRef(players);
  const guessesRef     = React.useRef(guesses);
  const answeredRef    = React.useRef(answered);

  React.useEffect(() => {
    messagesRef.current    = messages;
    playersRef.current     = players;
    guessesRef.current     = guesses;
    answeredRef.current    = answered;
  }, [messages, players, guesses, answered]);

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
    console.log("using effect");
    setGameStart(true);
    socket.on('connect', function() {
      console.log(`Websocket connected! Now joining room: ${roomId}`);
      socket.emit('join', {
        username,
        roomId,
      });
      console.log("done")
    });
  
    socket.on('disconnect', function() {
      console.log("websocket disconnected")
    });
  
    socket.on('receive_guess', function (data) {
      console.log(data);
      setMessages(messagesRef.current.concat(`${data.username}: ${data.guess}`));
    });
  
    socket.on('receive_answer', (data) => {
      console.log(data);
      setAnswered([...answeredRef.current, {username: data.username}]);
      setMessages([...messagesRef.current, `${data.username} guessed the word!`]);
    });
  
    socket.on('new_player_join', function (data) {
      console.log(data);
      setMessages(messagesRef.current.concat(`${data.username} has joined the room :D`));
    });
  
    socket.on('player_leave', function (data) {
      console.log(data);
      setMessages(messagesRef.current.concat(`${data.username} has left the room :(`));
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
      console.log("end game client");
      console.log(data);
      setModalToDisplay(GAME_END);
    });

    socket.on('choose_word', function (data) {
      console.log('Choosing Word', data.options);
      setWordChoices(data.options);
      setModalToDisplay(CHOOSE_WORD);
    });

    socket.on('close_word', function(data) {
      setModalToDisplay(NO_MODAL);
    })

    // disconnect the socket when component unmounts
    return () => {
      console.log("disconnecting...");
      socket.emit('leave', {
        username,
        roomId,
      });
      socket.disconnect();
    };
  }, []);

  const onChooseWord = (word) => {
    console.log("choosing: ", word);
    socket.emit("receive_word", {
      username,
      roomId,
      word,
    });
    setModalToDisplay(NO_MODAL);
  }

  const displayScreen = () => {
    if (gameStart) {
      return (
        <GamePlay
          socket={socket}
          guesses={guesses}
          messages={messages}
          setMessages={setMessages}
        />
      );
    }
    return <Lobby />;
  }

  const displayModalContent = () => {
    console.log(modalToDisplay);
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
        return (
          <ChooseWord
            choices={wordChoices}
            onChooseWord={onChooseWord}
          />
        );
      default:
        return (<span>Something's wrong with the screen display logic :(</span>);
    }
  }
  return (
    <>
      <Modal
        show={modalToDisplay !== NO_MODAL}
        onHide={() => setModalToDisplay(NO_MODAL)}
        backdrop='static'
        size="lg"
      >
        <Modal.Header>
          <Modal.Title style={{color: 'black'}}>
            {modalToDisplay}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {displayModalContent()}
        </Modal.Body>
      </Modal>
      { displayScreen() }
    </>
  )
}
export default withRouter(GameContainer);