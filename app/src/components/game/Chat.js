import React from 'react'
import { ListGroup, Container, Row, Col, Form, Button } from 'react-bootstrap';

export default function Chat(props) {
  return (
    <Container>
      <Row>
        <span style={{fontSize: '12pt', color: 'black'}}>Chat Window</span>
      </Row>
      <Row>
        <ListGroup>
          { props.messages.map((msg, idx) => {
            return (
              <ListGroup.Item
                key={idx}
                eventKey={idx}
                style={{fontSize:'12pt', color: 'black'}}
              >
                {msg}
              </ListGroup.Item>
            )
          }) }
        </ListGroup>
      </Row>
      <Form onSubmit={props.sendGuess} style={{
        position: 'absolute',
        bottom: '0'
      }}>
        <Row>
          <Col xs={10}>
              <Form.Control
                type="text"
                id="guess_input"
                placeholder="Enter your guess here"
                value={props.guess}
                onChange={(e) => props.setGuess(e.target.value)}
              />
          </Col>
          <Col xs={2}>
            <Button type="submit">Send</Button>
          </Col>
        </Row>
      </Form>
    </Container>
  )
}
