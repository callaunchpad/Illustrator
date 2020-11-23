/**
 * React component that sets up the socket listeners and contains
 * the canvas for drawing and guessing words
 */

import React from 'react'
import Sketch from "react-p5";
import { Container, Row, Col, ListGroup } from 'react-bootstrap';

import './Canvas.css';
// the global socket instance for this app
// import socket from '../../../socket';
const CANVAS_HEIGHT = 500;
const CANVAS_WIDTH  = 500;
export default function Canvas(props) {
  const [releasedPen, setReleasedPen] = React.useState(false);
  const [xPos, setXPos] = React.useState(0);
  const [yPos, setYPos] = React.useState(0);
  // set to true when it is the user's turn
  const [canDraw, setCanDraw] = React.useState(true);
  // text for the controlled form component. Contains the player's guess for the word
  const [guessText, setGuessText] = React.useState('');
  const [personDrawing, setPersonDrawing] = React.useState('');

  const { socket, roomId, drawer,username} = props;

  // sets up the p5 canvas when component mounts
  const setup = (p5, canvasParentRef) => {
    // use parent to render the canvas in this ref
    // (without that p5 will render the canvas outside of your component)

    // Callback function
    socket.on('receive_draw', data => {
      p5.stroke(data.color)
      p5.strokeWeight(data.strokeWidth)
      p5.line(data.x1, data.y1, data.x2, data.y2)
    });
    // socket.on('receive_drawer', data => {
    //   p5.stroke(data.color)
    //   p5.strokeWeight(data.strokeWidth)
    //   p5.line(data.x1, data.y1, data.x2, data.y2)
    // });

    socket.on('clear_canvas', data => {
      console.log('clearing canvas...');
      p5.clear();
    })

    p5.createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT).parent(canvasParentRef);
  };

  // function that is run when the user drags their mouse on the canvas
  // sends the mouse data to the server, which gets broadcasted to all players
  // in the same room
  const mouseDragged = (p5) => {
    // only allow user to draw if it is their turn
    if (username != drawer) {
      return;
    }
    if (p5.mouseX > CANVAS_WIDTH || p5.mouseY > CANVAS_HEIGHT || p5.mouseX < 0 || p5.mouseY < 0 ) {
      return;
    }
    setXPos(p5.mouseX);
    setYPos(p5.mouseY);

    // make these two dynamic based on state controlled inputs
    const color = 'rgba(100%,0%,100%,0.5)';
    const strokeWidth = 4;
    const penLifted = 0;
    p5.stroke(color)
    p5.strokeWeight(strokeWidth)
    p5.line(p5.pmouseX, p5.pmouseY, p5.mouseX, p5.mouseY);
    sendmouse(p5.pmouseX, p5.pmouseY, p5.mouseX, p5.mouseY, penLifted, color, strokeWidth)
  }

  const mouseReleased = (p5) => {
    const penLifted = 1;
    sendmouse(xPos, yPos, xPos, yPos, penLifted, 'rgba(100%,0%,100%,0.5)', 4);
  }

  // utility function for sending mouse stroke info to the server
  function sendmouse(x1, y1, x2, y2, penLifted, color, strokeWidth) {
    const data = {
      x1,
      y1,
      x2,
      y2,
      color,
      penLifted,
      strokeWidth,
      roomId,
    }
    socket.emit('send_draw', data)
    console.log("data")
    console.log(data)
  }

  // this is constantly run
  const draw = (p5) => {
    // NOTE: Do not use setState in the draw function or in functions that are executed
    // in the draw function...
    // please use normal variables or class properties for these purposes
  };

  // runs on form submission. Sends player's guess to server, which broadcasts it to all other players
  // in the same room
  const guessWord = (e) => {
    e.preventDefault();
    console.log('guessed: ', guessText)
    const data = {guessText, roomId}
    socket.emit('send_guess', data)
    console.log('emitted: ', guessText)
    // emit a websocket event
    setGuessText('')
  }

  // return a really crappy Canvas component that'll be beautiful later
  return (
    
    <Container>
      {/* <p>Choose color (# hex)</p>
      <input type="text" name="custom_color" placeholder="#FFFFFF" id="pickcolor" className="call-picker" />
      <div id="color-holder" className="color-holder call-picker"></div>
      <button id="color-btn">Change color</button>
      <br />
      <p>Choose stroke width</p>
      <input type="text" name="stroke_width" placeholder="4" id="stroke-width-picker" className="stroke_width_picker" />
      <button id="stroke-btn">Change stroke width</button> */}

      {/* This is the p5 react component */}
      <Row>
        <Sketch
          style={{
            backgroundColor: 'white',
          }}
          setup={setup}
          draw={draw}
          mouseDragged={mouseDragged}
          mouseReleased={mouseReleased}
        />
      </Row>

      
      {/* <form onSubmit={guessWord}>
        <label>
          Guess:
          <input type="text" value={guessText} onChange={(e) => setGuessText(e.target.value)} />
        </label>
        <input type="submit" value="Submit" />
      </form> */}
      <button onClick={() => socket.emit('test_sketch_rnn', {roomId})}>Test Sketch Rnn</button>
      {/* <button onClick={() => {console.log("joining room..."); socket.emit('join', {roomId: 1, username: 'hello'})}}>Join room</button> */}
    </Container>
  )
}
