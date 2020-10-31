import React from 'react';
import GlobalContext from '../../context';
import Canvas from './canvas/Canvas';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

import Chat from './Chat';
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
        <Form onSubmit={startGame}>
          <Button type="submit">Start Game</Button>
        </Form>
      </Row>
      <Row>
        <Col xs={7}>
          <Canvas
            socket={props.socket}
          />
        </Col>
        <Col xs={5} style={{backgroundColor: 'white'}}>
          {/* chat goes here! */}
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
