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
const NO_MODAL  = 'No modal';
const GAME_START  = 'game_start';
const CHOOSE_WORD = "Pick a word!"

// let wordResolve;

function GameContainer(props) {
  const [socket, _] = React.useState(socketIOClient(ENDPOINTS.root));
  const [gameStart, setGameStart] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);

  const [messages, setMessages] = React.useState([]); // list of strings that are displayed in the canvas chat
  const [players, setPlayers]   = React.useState([]); // list of players that joined
  const [guesses, setGuesses]   = React.useState([]); // list of player names and their guesses
  const [answered, setAnswered] = React.useState([]); // list of players that guessed the word
  const [wordChoices, setWordChoices] = React.useState([]); // list of word choices to be displayed
  const [leaderboard, setLeaderboard] = React.useState({});
  const [chosenWord, setChosenWord] = React.useState('');

  const messagesRef = React.useRef(messages);
  const playersRef  = React.useRef(players);
  const guessesRef  = React.useRef(guesses);
  const answeredRef = React.useRef(answered);
  const leaderboardRef = React.useRef(leaderboard);
  React.useEffect(() => {
    messagesRef.current = messages;
    playersRef.current  = players;
    guessesRef.current  = guesses;
    answeredRef.current = answered;
    leaderboardRef.current = leaderboard;
  }, [messages, players, guesses, answered, leaderboard]);

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
    socket.on('connect', function() {
      console.log(`Websocket connected! Now joining room: ${roomId}`);
      socket.emit('join', {
        username,
        roomId,
      });
    });
  
    socket.on('disconnect', function() {
      console.log("websocket disconnected")
    });
  
    socket.on('receive_guess', function (data) {
      setMessages(messagesRef.current.concat(`${data.username}: ${data.guess}`));
    });
  
    socket.on('receive_answer', (data) => {
      setAnswered([...answeredRef.current, {username: data.username}]);
      setMessages([...messagesRef.current, `${data.username} guessed the word!`]);
    });
  
    socket.on('new_player_join', function (data) {
      setMessages(messagesRef.current.concat(`${data.username} has joined the room :D`));
      let copy = JSON.parse(JSON.stringify(leaderboardRef.current));
      copy[data.username] = 0;
      setLeaderboard(copy);
    });
  
    socket.on('player_leave', function (data) {
      setMessages(messagesRef.current.concat(`${data.username} has left the room :(`));
    });

    socket.on('new_game', function (data) {
      // setModalToDisplay(GAME_START)
      socket.emit('start', {
        username,
        roomId,
      });
    });

    socket.on('end_game', function (data) {
      console.log("end game client");
      setModalToDisplay(GAME_END);
    });

    socket.on('choose_word', async (data) => {
      console.log('Choosing Word', data.options);
      setWordChoices(data.options);
      setModalToDisplay(CHOOSE_WORD);

      // const word = await chooseWord();
      // console.log("choose_word: ", word);
      // return { word, }
    });

    socket.on('close_word', function(data) {
      setModalToDisplay(NO_MODAL);
    });

    socket.on('show_leaderboard', function (data) {
      console.log('leaderboard: ', data);
      setLeaderboard(data.leaderboard);
    })

    socket.on('reveal_letter', function (data) {
      console.log('reveal letter: ', data);
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
  // returns a promise that resolves once the onChooseWord button handler runs
  // this promise will therefore resolve only when the user has chosen a word/times out
  // const chooseWord = async (choices) => {
  //   console.log("running chooseword...");
  //   setModalToDisplay(CHOOSE_WORD);
  //   const p = new Promise((resolve, reject) => {
  //     wordResolve = resolve;
  //   });
  //   return p;
  // }

  const onChooseWord = (word) => {
    console.log("running on choose word: ", word);
    socket.emit("receive_word", {
      username,
      roomId,
      word,
    });
    setChosenWord(word);
    // wordResolve(word);
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
          leaderboard={leaderboard}
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