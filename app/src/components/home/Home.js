import axios from 'axios';
import React from 'react';
import { withRouter } from 'react-router-dom';

import endpoints from '../../endpoints';

function Home(props) {
  const {
    username,
    roomId,
    setRoomId,
    setUsername,
  } = props;
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(endpoints.game, {
        username,
        roomId,
      });
      if (res.data.success) {
        props.history.push({
          pathname: '/game',
          // search: '?query=abc',
          state: {
            roomId,
          },
        });
      } else {
        alert(`could not join the room with room id: ${roomId}`);
      }
    } catch(e) {
      console.log(e);
    }
  }

  return (
    <div className='home container'>
      <form onSubmit={handleSubmit}>
        <div>
          <label>What's your username?</label>
          <input
            type="text"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Enter room id:</label>
          <input
            type="text"
            name="roomId"
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
          />
        </div>
        <button type="submit">Join Room!</button>
      </form>
    </div>
  )
}
export default withRouter(Home);