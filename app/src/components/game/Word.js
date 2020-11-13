import React from 'react'
import { Container, ListGroup, Row, Col, Form, Button, Modal } from 'react-bootstrap';
export default function Word(props) {
  // takes in a list of players and their scores
  const { chosenWord, revealLetter } = props;
  console.log("OMG IT WORKED! " + chosenWord);

  function setCharAt(str, index, chr) {
    if(index > str.length - 1) return str;
    return str.substring(0,index) + chr + str.substring(index+1);
  }

  const placeholder = '_';
  let str = placeholder.repeat(chosenWord.length);
  var index;
  for (index = 0; index < revealLetter.length; index++) { 
    str = setCharAt(str, revealLetter[index][0], revealLetter[index][1]);
  } 

  return (
    <Container style={{padding: 0}}>
    <p>THIS IS THE GUESSING THING: </p>
      <p style="letter-spacing: 5;">{str}</p>
    </Container>
  )
}
