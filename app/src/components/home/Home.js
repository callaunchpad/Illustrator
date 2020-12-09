import axios from 'axios';
import React from 'react';
import { withRouter } from 'react-router-dom';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import endpoints from '../../endpoints';
import './Home.css';
import logo from './illustrator_logo.png';

import socket from '../../socket';

function Home(props) {
  const {
    username,
    roomId,
    setRoomId,
    setUsername,
  } = props;

  React.useEffect(() => {
    console.log("home use effect");
  }, []);

  
  const handleCreateAndJoin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(endpoints.game, {
        username,
        roomId,
      });
      const { too_many, duplicate, create, join } = res.data;
      if (create) {
        // emit create game event
        let room = Math.random().toString(36).substring(7);
        console.log(`Generating room id and creating game...`);
        console.log(`room id is ${room}`);
        setRoomId(room);
        socket.emit('create_room', {
          username,
          'roomId': room,
        });
      } else if (join) {
        if (duplicate) {
          alert(`A user with username ${username} already exists in room ${roomId}`);
          return;
        }
        if (too_many) {
          alert(`This room already has 8 people in it :(`);
          return;
        }
        console.log(`Websocket connected! Now joining room: ${roomId}`);
        socket.emit('join', {
          username,
          roomId,
        });
      } else {
        alert("Please enter a username :)");
        return;
      }
      props.history.push({
        pathname: '/game',
        state: { roomId },
      });
    } catch(e) {
      alert("something went wrong with your request to the server :(");
      console.log(e);
    }
  }

  // const handleJoin = async (e) => {
  //   e.preventDefault();
  //   try {
  //     const res = await axios.post(endpoints.game, {
  //       username,
  //       roomId,
  //     });
  //     if (res.data.join) {
  //       props.history.push({
  //         pathname: '/game',
  //         // search: '?query=abc',
  //         state: {
  //           roomId,
  //         },
  //       });
  //     } else {
  //       alert(`Could not join the room with room id: ${roomId}`);
  //     }
  //   } catch(e) {
  //     console.log(e);
  //   }
  // }

  return (
    <Container>
      <Row className="justify-content-md-center">
        <img src={logo}></img>
      </Row>
      <Form>
        <Form.Group controlId="formName">
          {/* <Form.Label style={{color: 'white'}}>Name</Form.Label> */}
          <Form.Row className="justify-content-md-center">
            <Col xs={4}>
              <Form.Control
                type="text"
                placeholder="Enter name..."
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />

            </Col>
          </Form.Row>
            <div class="pad"></div>
            <Button variant="outline-light" onClick={handleCreateAndJoin}>
              Create Room
            </Button>
          
        </Form.Group>
        

        <Form.Group controlId="formRoomId">
          {/* <Form.Label style={{color: 'white'}}>Room Id</Form.Label> */}
          <Form.Row className="justify-content-md-center">
            <Col xs={4}>
              <Form.Control
                type="text"
                placeholder="Room id..."
                value={roomId}
                onChange={(e) => setRoomId(e.target.value)}
              />
            </Col>
          </Form.Row>
          <div class="pad"></div>
          <Button class="button" variant="outline-light" onClick={handleCreateAndJoin}>
            Join Room
          </Button>
        </Form.Group>
        
      </Form>
    </Container>
  )
}
export default withRouter(Home);