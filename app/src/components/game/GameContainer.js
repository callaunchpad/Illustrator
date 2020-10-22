/**
 * A container component that displays different screens
 * depending on the game state. All client socket logic is here.
 * By the time this component is displayed, the client should have already
 * joined a room and should already have a username
 */

import React from 'react'
import Modal from '@material-ui/core/Modal';
import { withRouter } from 'react-router-dom';

import End from './screens/End';
import socket from '../../socket';
import Lobby from './Lobby';
import TimesUp from './screens/TimesUp';
import setUpSocket from './socketHandlers';
import GamePlay from './GamePlay';
import GlobalContext from '../../context';

const GAME_END  = 'game_end';
const TIME_UP   = 'time up';
const NO_MODAL  = 'none';
function GameContainer(props) {
  const [gameStart, setGameStart] = React.useState(false);
  const [modalToDisplay, setModalToDisplay] = React.useState(NO_MODAL);
  const [guesses, setGuesses] = React.useState([]);

  const globalContext = React.useContext(GlobalContext);
  // console.log(props.location.state.roomId);
  const { username, roomId } = globalContext;
  if (username === undefined || username.length === 0 || roomId === undefined || roomId.length === 0) {
    props.history.push("/");
  }

  React.useEffect(() => {
    console.log("using effect....");
    // redirect to home page if no username or roomId exists
    // change this later so that username and roomId persists in local storage until the game finishes
    setUpSocket(
      username,
      roomId,
      guesses,
      setGuesses,
      modalToDisplay,
      setModalToDisplay,
    );
  }, []);

  const displayScreen = () => {
    if (gameStart) {
      return <GamePlay guesses={guesses}/>;
    }
    return <Lobby />;
  }

  const displayModalContent = () => {
    switch(modalToDisplay) {
      case NO_MODAL:
        return null;
      case GAME_END:
        return <End />;
      case TIME_UP:
        return <TimesUp />;
      default:
        return (<span>Something's wrong with the screen display logic :(</span>);
    }
  }
  console.log(modalToDisplay);
  console.log(modalToDisplay !== NO_MODAL);
  return (
    <div className='game container'>
      { displayScreen() }
      <Modal
        open={modalToDisplay !== NO_MODAL}
        onClose={() => setModalToDisplay(NO_MODAL)}
      >
        <div>
          <h1 style={{color: 'white'}}>{modalToDisplay}</h1>
          {displayModalContent()}
        </div>
      </Modal>
    </div>
  )
}
export default withRouter(GameContainer);