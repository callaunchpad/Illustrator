/**
 * React component that sets up the socket listeners and contains
 * the canvas for drawing and guessing words
 */

import React from 'react'
import Sketch from "react-p5";

import './Canvas.css';
// the global socket instance for this app
import socket from '../../../socket';

export default function Canvas(props) {
  // set to true when it is the user's turn
  const [canDraw, setCanDraw] = React.useState(true);
  // text for the controlled form component. Contains the player's guess for the word
  const [guessText, setGuessText] = React.useState('');

  // sets up the p5 canvas when component mounts
  const setup = (p5, canvasParentRef) => {
    // use parent to render the canvas in this ref
    // (without that p5 will render the canvas outside of your component)

    // Callback function
    socket.on('receive_draw', data => {
      console.log(data)
      p5.stroke(data.color)
      p5.strokeWeight(data.strokeWidth)
      p5.line(data.x, data.y, data.pX, data.pY)
    })

    console.log("setting up...")
    p5.createCanvas(500, 500).parent(canvasParentRef);
  };

  // function that is run when the user drags their mouse on the canvas
  // sends the mouse data to the server, which gets broadcasted to all players
  // in the same room
  const mouseDragged = (p5) => {
    // only allow user to draw if it is their turn
    if (!canDraw) {
      return
    }

    // make these two dynamic based on state controlled inputs
    const color = 'rgba(100%,0%,100%,0.5)'
    const strokeWidth = 4
    p5.stroke(color)
    p5.strokeWeight(strokeWidth)
    p5.line(p5.mouseX, p5.mouseY, p5.pmouseX, p5.pmouseY);
    sendmouse(p5.mouseX, p5.mouseY, p5.pmouseX, p5.pmouseY, color, strokeWidth)
  }

  // utility function for sending mouse stroke info to the server
  function sendmouse(x, y, pX, pY, color, strokeWidth) {
    const data = {
      x,
      y,
      pX,
      pY,
      color,
      strokeWidth,
      roomId: 1
    }
    socket.emit('send_draw', data)
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
    const data = {guessText, roomId: 1}
    socket.emit('send_guess', data)
    console.log('emitted: ', guessText)
    // emit a websocket event
    setGuessText('')
  }

  // return a really crappy Canvas component that'll be beautiful later
  return (
    <div>
      <p>Choose color (# hex)</p>
      <input type="text" name="custom_color" placeholder="#FFFFFF" id="pickcolor" className="call-picker" />
      <div id="color-holder" className="color-holder call-picker"></div>
      <button id="color-btn">Change color</button>
      <br />
      <p>Choose stroke width</p>
      <input type="text" name="stroke_width" placeholder="4" id="stroke-width-picker" className="stroke_width_picker" />
      <button id="stroke-btn">Change stroke width</button>

      {/* This is the p5 react component */}
      <Sketch setup={setup} draw={draw} mouseDragged={mouseDragged}/>
      
      <form onSubmit={guessWord}>
        <label>
          Guess:
          <input type="text" value={guessText} onChange={(e) => setGuessText(e.target.value)} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      <button onClick={() => socket.emit('test_sketch_rnn', {roomId: 1})}>Test Sketch Rnn</button>
      <button onClick={() => {console.log("joining room..."); socket.emit('join', {roomId: 1, username: 'hello'})}}>Join room</button>
    </div>
  )
}
