/**
 * A container component that displays different screens
 * depending on the game state. All client socket logic is here.
 * By the time this component is displayed, the client should have already
 * joined a room and should already have a username
 */

import React from 'react'
import { withRouter } from 'react-router-dom';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';

import End from './screens/End';
import Lobby from './Lobby';
import TimesUp from './screens/TimesUp';
import StartGame from './screens/StartGame';
import GamePlay from './GamePlay';
import GlobalContext from '../../context';
import { CardActionArea } from '@material-ui/core';
import ChooseWord from './screens/ChooseWord';

import socket from '../../socket'

const GAME_END  = 'game_end';
const TIME_UP   = 'time up';
const NO_MODAL  = 'No modal';
const GAME_START  = 'game_start';
const CHOOSE_WORD = "Pick a word!";

function GameContainer(props) {
  // const [socket, _] = React.useState(socketIOClient(ENDPOINTS.root));
  const [gameStarted, setGameStarted] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);

  const [messages, setMessages] = React.useState([]); // list of strings that are displayed in the canvas chat
  const [players, setPlayers]   = React.useState([]); // list of players that joined
  const [guesses, setGuesses]   = React.useState([]); // list of player names and their guesses
  const [answered, setAnswered] = React.useState([]); // list of players that guessed the word
  const [wordChoices, setWordChoices] = React.useState([]); // list of word choices to be displayed
  const [leaderboard, setLeaderboard] = React.useState({});
  const [chosenWord, setChosenWord] = React.useState('');
  const [revealLetter, setRevealLetter] = React.useState([]);
  // const [roomIdState, setRoomIdState] = React.useState('');
  const [drawer, setDrawer] = React.useState('');
  const [isTimerStarted, setIsTimerStarted] = React.useState(false); // toggle to start/stop timer

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
  // redirect to home page if user or room id does not exist
  // this will typically happen if the user refreshes
  // can make this more robust laster by storing username, roomid in localstorage
  // var newRoomId = '';
  const { username, roomId } = globalContext;

  React.useEffect(() => {
    console.log(username, roomId);
    if (username === undefined || username.length === 0) {
      console.log("No username");
      props.history.push("/");
    }
  
    socket.on('disconnect', function() {
      console.log("websocket disconnected")
    });
  
    socket.on('receive_guess', function (data) {
      setMessages(messagesRef.current.concat(`${data.username}: ${data.guess}`));
    });

    socket.on('receive_own_guess', function (data) {
      setMessages(messagesRef.current.concat("YOU CANNOT GUESS DURING YOUR TURN!"));
    });
    socket.on('already_guessed', function (data) {
      setMessages(messagesRef.current.concat("YOU ALREADY GOT POINTS!"));
    });
  
    socket.on('receive_answer', (data) => {
      setAnswered([...answeredRef.current, {username: data.username}]);
      setMessages([...messagesRef.current, `${data.username} guessed the word!`]);
    });
  
    socket.on('new_player_join', function (data) {
      setMessages(messagesRef.current.concat(`${data.username} has joined the room :D`));
      // let copy = JSON.parse(JSON.stringify(leaderboardRef.current));
      // console.log("new leaderboard: ", copy);
      // copy[data.username] = 0;
      // setLeaderboard(copy);
    });
  
    socket.on('player_leave', function (data) {
      setMessages(messagesRef.current.concat(`${data.username} has left the room :(`));
    });

    socket.on('new_game', function (data) {
      // setModalToDisplay(GAME_START)
      console.log("starting actual game: ");
      console.log(data);
      setGameStarted(true);
      socket.emit('start', {
        username,
        'roomId': roomId,
      });
    });

    socket.on('start_game', function (data) {
      setGameStarted(true);
    });

    socket.on('end_game', function (data) {
      console.log("end game client");
      // setGameStarted(false);
      setGameStarted(true);
      setModalToDisplay(GAME_END);
    });

    socket.on('not_choose_word', async (data) => {
      console.log('Not choosing word', data.player_username);
    });
    
    socket.on('choose_word', async (data) => {
      console.log('Choosing Word', data.options);
      setWordChoices(data.options);
      setModalToDisplay(CHOOSE_WORD);
    });

    socket.on('set_drawer', async (data) => {
      setDrawer(data.username);
    });

    socket.on('close_word', function(data) {
      setModalToDisplay(NO_MODAL);
      console.log(data);
      if (data && data.word) {
        alert(`You are drawing: ${data.word}`);
      }
    });

    // the round officialy ends when this is sent
    socket.on('show_leaderboard', function (data) {
      console.log('leaderboard: ', data);
      setLeaderboard(data.leaderboard);
    });

    socket.on('draw_end', function (data) {
      console.log("drawing finished");
      setIsTimerStarted(false);
    });
    
    // this is when the round officially starts with the drawing
    socket.on('establish_word', function (data) {
      setChosenWord(data.word);
      setIsTimerStarted(true);
      console.log('establish word: ', data.word);
    })

    socket.on('reveal_letter', function (data) {
      setRevealLetter(data.show);
      // console.log('reveal letter: ', data.show);
    })

    // disconnect the socket when component unmounts
    return () => {
      console.log("leaving...");
      socket.emit('leave', {
        username,
        'roomId': roomId,
      });
      // socket.disconnect();
    };
  }, []);

  const onChooseWord = (word) => {
    console.log("running on choose word: ", word);
    socket.emit("receive_word", {
      username,
      'roomId': roomId,
      word,
    });
    setChosenWord(word);
    setModalToDisplay(NO_MODAL);
  }

  const displayScreen = () => {
    return (
      <GamePlay
        guesses={guesses}
        messages={messages}
        setMessages={setMessages}
        gameStarted={gameStarted}
        setGameStarted={setGameStarted}
        leaderboard={leaderboard}
        chosenWord={chosenWord}
        revealLetter={revealLetter}
        roomId={roomId}
        drawer={drawer}
        username={username}
        isTimerStarted={isTimerStarted}
      />
    );
  }

  const displayModalContent = () => {
    // console.log(modalToDisplay);
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