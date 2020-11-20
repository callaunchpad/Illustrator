import axios from 'axios';
import React from 'react';
import { withRouter } from 'react-router-dom';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import endpoints from '../../endpoints';
import './Home.css';
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

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(endpoints.game, {
        username,
        roomId,
      });
      if (res.data.create) {
        props.history.push({
          pathname: '/game',
          // search: '?query=abc',
          state: {
            roomId,
          },
        });
      } else {
        alert(`Please make a username!`);
      }
    } catch(e) {
      console.log(e);
    }
  }

  const handleJoin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(endpoints.game, {
        username,
        roomId,
      });
      if (res.data.join) {
        props.history.push({
          pathname: '/game',
          // search: '?query=abc',
          state: {
            roomId,
          },
        });
      } else {
        alert(`Could not join the room with room id: ${roomId}`);
      }
    } catch(e) {
      console.log(e);
    }
  }

  return (
    <Container>
      <Form>
        <Form.Group controlId="formName">
          {/* <Form.Label style={{color: 'white'}}>Name</Form.Label> */}
          <Form.Row>
            <Col>
              <Form.Control
                type="text"
                placeholder="Enter name..."
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Col>
            <Col>
              <Button variant="primary" onClick={handleCreate}>
                Create Room
              </Button>
            </Col>
          </Form.Row>
        </Form.Group>

        <Form.Group controlId="formRoomId">
          {/* <Form.Label style={{color: 'white'}}>Room Id</Form.Label> */}
          <Form.Row>
            <Col>
              <Form.Control
                type="text"
                placeholder="Room id..."
                value={roomId}
                onChange={(e) => setRoomId(e.target.value)}
              />
            </Col>
          </Form.Row>
          
        </Form.Group>
        <Button variant="primary" onClick={handleJoin}>
          Join Room
        </Button>
      </Form>
      {/* <form className='form' onSubmit={handleSubmit}>
        <Container>
          <Row>
            <Col xs={2}>
              <label>Name:</label>
            </Col>
            <Col>
              <input
                type="text"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Col>
          </Row>
          <Row>
            <label>Join a room:</label>
            <input
              placeholder='room id...'
              type="text"
              name="roomId"
              value={roomId}
              onChange={(e) => setRoomId(e.target.value)}
            />
          </Row>
          <Row>
            <button type="submit">Join Room!</button>
          </Row>
        </Container>
      </form> */}
    </Container>
  )
}
export default withRouter(Home);