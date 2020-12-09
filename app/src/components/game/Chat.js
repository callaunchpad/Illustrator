import React from 'react'
import { ListGroup, Container, Row, Col, Form, Button } from 'react-bootstrap';

export default function Chat(props) {
  const { messages, isTimerStarted, sendGuess, setGuess, guess } = props;
  const messageRef = React.useRef(null);
  React.useEffect(() => {
    if (messageRef.current && isTimerStarted) {
      console.log("scrolling into view!");
      messageRef.current.scrollIntoView(false, { behavior: "smooth" });
    }
  }, [messages])
  return (
    <Container style={{
      height: '100%',
    }}>
      <Row>
        <span style={{fontSize: '12pt', color: 'black', fontWeight: 'bold', textAlign: 'center', paddingTop: '5px'}}>Chat Window</span>
      </Row>
      <Row style={{
        overflowY: 'auto',
        height: `calc(100% - 50px)`,
        maxHeight: '45vh',
        display: 'flex',
        flexDirection: 'column',
        border: 'solid'
      }}>
        <ListGroup style={{width: '100%'}}>
          { messages.map((msg, idx) => {
            if (idx == messages.length - 1) {
              return (
                <React.Fragment key={messages.length}>                
                  <ListGroup.Item
                    key={idx}
                    eventKey={idx}
                    style={{
                      fontSize:'12pt',
                      color: 'black',
                      padding: 0,
                      border: 'none',
                      paddingTop: '3px',
                      textAlign: 'left',
                    }}
                  >{msg}</ListGroup.Item>
                  {/* dummy div for autoscrolling */}
                  <div
                    key={messages.length}
                    style={{ float:"left", clear: "both", height: "0"}}
                    ref={messageRef}>
                  </div>
                </React.Fragment>
              )
            } else {
              return (
                <ListGroup.Item
                  key={idx}
                  eventKey={idx}
                  style={{
                    fontSize:'12pt',
                    color: 'black',
                    padding: 0,
                    border: 'none',
                    paddingTop: '3px'
                  }}
                >{msg}</ListGroup.Item>
              )
            }
          }) }
        </ListGroup>
      </Row>
      <Form onSubmit={sendGuess} style={{
        position: 'absolute',
        bottom: '10px',
        left: '10px',
        right: '10px',
        width: '95%',
      }}>
        <Row>
          <Col xs={12}>
            <Form.Control
              type="text"
              id="guess_input"
              placeholder={isTimerStarted ? "Enter your guess here" : ""}
              value={guess}
              disabled={!isTimerStarted}
              onChange={(e) => setGuess(e.target.value)}
            />
          </Col>
        </Row>
      </Form>
    </Container>
  )
}
