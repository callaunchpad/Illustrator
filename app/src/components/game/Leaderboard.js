import React from 'react'
import { Container, ListGroup, Row, Col, Form, Button, Modal } from 'react-bootstrap';
export default function Leaderboard(props) {
  // takes in a list of players and their scores
  const { players } = props;
  return (
    <Container>
      <ListGroup>
        {/* { players.map((player, idx) => {
          return (
            <ListGroup.Item>{`${player.name}: ${player.score}`}</ListGroup.Item>
          )
        })} */}
        <ListGroup.Item>Cras justo odio</ListGroup.Item>
        <ListGroup.Item>Dapibus ac facilisis in</ListGroup.Item>
        <ListGroup.Item>Morbi leo risus</ListGroup.Item>
        <ListGroup.Item>Porta ac consectetur ac</ListGroup.Item>
        <ListGroup.Item>Vestibulum at eros</ListGroup.Item>
      </ListGroup>
    </Container>
  )
}
