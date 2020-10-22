/**
 * The App component is the usually the "root" of a React app.
 * It defines the overall layout of the application and any global state variables
 * are typically set here.
 */

import React from 'react';
import { BrowserRouter, Route, Switch, useHistory, withRouter } from 'react-router-dom';

import './App.css';
import logo from './logo.svg';

import GlobalContext from './context';
import Home from './components/home/Home';
import GameContainer from './components/game/GameContainer';
const axios = require('axios');

function App(props) {
  const [username, setUsername] = React.useState('');
  const [roomId, setRoomId]     = React.useState('');
  return (
    <div className="App">
      <header className="App-header">
        <GlobalContext.Provider value={{
          username,
          roomId,
        }}>
          <BrowserRouter>
            <Switch>
              <Route exact path='/'>
                <Home
                  username={username}
                  roomId={roomId}
                  setUsername={setUsername}
                  setRoomId={setRoomId}
                />
              </Route>
              <Route path='/game'>
                <GameContainer />
              </Route>
            </Switch>
          </BrowserRouter>
        </GlobalContext.Provider>
      </header>
    </div>
  );
}

export default App;
