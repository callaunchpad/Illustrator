/**
 * The App component is the usually the "root" of a React app.
 * It defines the overall layout of the application and any global state variables
 * are typically set here.
 */

import React from 'react';
import logo from './logo.svg';
import './App.css';

import Canvas from './components/canvas/Canvas'
const axios = require('axios');

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <Canvas />
      </header>
    </div>
  );
}

export default App;
