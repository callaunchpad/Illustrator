/**
 * React component that sets up the socket listeners and contains
 * the canvas for drawing and guessing words
 */

import React from 'react'
import Sketch from "react-p5";
import { Container, Row } from 'react-bootstrap';

import './Canvas.css';
// the global socket instance for this app
import socket from '../../../socket';
const CANVAS_HEIGHT = 500;
const CANVAS_WIDTH  = 500;
export default function Canvas(props) {
  var shouldClear = false;
  const [xPos, setXPos] = React.useState(0);
  const [yPos, setYPos] = React.useState(0);
  const { roomId, drawer, username, isTimerStarted } = props;

  // sets up the p5 canvas when component mounts
  const setup = (p5, canvasParentRef) => {
    // use parent to render the canvas in this ref
    // (without that p5 will render the canvas outside of your component)
    // Callback function
    console.log("setting up canvas...");
    socket.on('receive_draw', data => {
      // means the previous data point has penLifted = true
      // don't connect the previous point to this one
      p5.stroke(data.color);
      p5.strokeWeight(data.strokeWidth);
      p5.line(data.x1, data.y1, data.x2, data.y2);
    });

    socket.on('clear_canvas', data => {
      p5.clear();
    });

    // only set up the canvas and manipulate the dom if it's mounted
    if (canvasParentRef) {
      p5.createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT).parent(canvasParentRef);
    }
  };

  // function that is run when the user drags their mouse on the canvas
  // sends the mouse data to the server, which gets broadcasted to all players
  // in the same room
  const mouseDragged = (p5) => {
    // only allow user to draw if it is their turn and we are allowing drawings to happen
    if (!isTimerStarted || username != drawer) {
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
    if (!isTimerStarted || username != drawer) { return; }
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
    };
    socket.emit('send_draw', data);
    console.log("data");
    console.log(data);
  }

  // this is constantly run
  const draw = (p5) => {
    // NOTE: Do not use setState in the draw function or in functions that are executed
    // in the draw function...
    // please use normal variables or class properties for these purposes
    if (shouldClear) {
      p5.clear();
      socket.emit('artist_cleared', { roomId });
      shouldClear = false;
    }
  };

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
            paddingLeft: '10px',
          }}
          setup={setup}
          draw={draw}
          mouseDragged={mouseDragged}
          mouseReleased={mouseReleased}
        />
      </Row>
      <button class="clear_button" onClick={() => {
        if (isTimerStarted && username == drawer) {
          shouldClear = true;
        }
      }}>Clear Drawing</button>
    </Container>
  )
}
