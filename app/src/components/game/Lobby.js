/**
 * A component for displaying the waiting lobby. This 
 * is shown before the game actually starts, and players
 * can join or leave freely.
 */

import React from 'react'
import GlobalContext from '../../context';
export default function Lobby() {
  const globalContext = React.useContext(GlobalContext);
  const { username, roomId } = globalContext;

  return (
    <div className='lobby container'>
      <h1>Welcome to room {roomId}</h1>
    </div>
  )
}
