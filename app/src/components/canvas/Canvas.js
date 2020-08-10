import React from 'react'
import Sketch from "react-p5";
import socketIOClient from "socket.io-client";

import ENDPOINTS from '../../endpoints';
import './Canvas.css';


export default function Canvas() {
  const socket = socketIOClient(ENDPOINTS.root);
  // set to true when it is the user's turn
  const [canDraw, setCanDraw] = React.useState(true)
  React.useEffect(() => {
    const asyncUseEffect = async () => {
      // verify our websocket connection is established
      socket.on('connect', function() {
        console.log('Websocket connected!');
      });

      socket.on('receive_guess', function(guess) {
        console.log(`received guess: ${guess}`)
      })

      socket.on('disconnect', function() {
        console.log("websocket disconnected")
      })
    }
    asyncUseEffect()
  }, [])

  const setup = (p5, canvasParentRef) => {
    // use parent to render the canvas in this ref
    // (without that p5 will render the canvas outside of your component)

    // Callback function
    socket.on('receive_draw', data => {
      p5.stroke(data.color)
      p5.strokeWeight(data.strokeWidth)
      p5.line(data.x, data.y, data.pX, data.pY)
    })

    console.log("setting up...")
    p5.createCanvas(500, 500).parent(canvasParentRef);
  };


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

  function sendmouse(x, y, pX, pY, color, strokeWidth) {
    const data = {
      x,
      y,
      pX,
      pY,
      color,
      strokeWidth,
    }
    socket.emit('send_draw', data)
  }

  // this is constantly run
  const draw = (p5) => {
    // NOTE: Do not use setState in the draw function or in functions that are executed
    // in the draw function...
    // please use normal variables or class properties for these purposes
  };

  return (
    <div>
      <p>Choose color (# hex)</p>
      <input type="text" name="custom_color" placeholder="#FFFFFF" id="pickcolor" class="call-picker" />
      <div id="color-holder" class="color-holder call-picker"></div>
      <button id="color-btn">Change color</button>
      <br />
      <p>Choose stroke width</p>
      <input type="text" name="stroke_width" placeholder="4" id="stroke-width-picker" class="stroke_width_picker" />
      <button id="stroke-btn">Change stroke width</button>
      <Sketch setup={setup} draw={draw} mouseDragged={mouseDragged}/>
    </div>
  )
}
