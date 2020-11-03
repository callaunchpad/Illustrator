import React from 'react'
import { Container, ListGroup, Row, Col, Form, Button, Modal } from 'react-bootstrap';
export default function Leaderboard(props) {
  // takes in a list of players and their scores
  const { leaderboard } = props;
  console.log(leaderboard);
  return (
    <Container style={{padding: 0}}>
      <ListGroup>
        { Object.keys(leaderboard).map((username, idx) => {
          // kv is a 2 element array. 0th entry is username, 1st is score
          return (
            <ListGroup.Item
              key={idx}
              style={{color: 'black', fontSize: '12pt'}}
            >
              {`${username}: ${Math.floor(leaderboard[username])}`}
            </ListGroup.Item>
          )
        })}
      </ListGroup>
    </Container>
  )
}
