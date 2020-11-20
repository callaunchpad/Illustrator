import React from 'react';
import GlobalContext from '../../context';
import Canvas from './canvas/Canvas';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

import Chat from './Chat';
import Leaderboard from './Leaderboard';
import Word from './Word';

export default function GamePlay(props) {
  const [guess, setGuess] = React.useState('');
  const globalContext = React.useContext(GlobalContext);
  const { username } = globalContext;
  const { roomId } = props;
  const sendGuess = (e) => {
    // props.setMessages(props.messages.concat("hello"));
    // console.log('messages: ', props.messages);
    e.preventDefault();
    let g = guess.trim();
    if (g.length) {
      props.socket.emit('send_guess', {
        username,
        roomId,
        guess: g,
      });
    }
    setGuess('');
  }
  const startGame = (e) => {
    e.preventDefault();
    props.socket.emit('start_game', {
        username,
        roomId: roomId
    });
  }
  return (
    <Container>
      <Row>
        <Col xs={2}>
          <Form onSubmit={startGame}>
            <Button type="submit">Start Game</Button>
          </Form>
        </Col>
        <Col xs={6}>
        <p>The room id is: {roomId}</p>
        </Col> 
      </Row>
      <Row>
        <Word
            chosenWord={props.chosenWord}
            revealLetter={props.revealLetter}
        />
      </Row>
      <Row>
        <Col xs={2} style={{
          backgroundColor: 'white',
          padding: 0,
          
        }}>
          <Leaderboard
            leaderboard={props.leaderboard}
          />
        </Col>
        <Col xs={6}>
          <Canvas
            socket={props.socket}
            roomId={props.roomId}
          />
        </Col>
        <Col xs={4} style={{backgroundColor: 'white'}}>
          <Chat
            messages={props.messages}
            sendGuess={sendGuess}
            setGuess={setGuess}
            guess={guess}
          />
        </Col>
      </Row>
    </Container>
  )
}
