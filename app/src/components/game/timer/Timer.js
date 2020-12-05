import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

const ROUND_LENGTH = 30; // number of seconds ppl have to guess. Remove this if we add settings for create game.

export default function Timer(props) {
  const { isTimerStarted } = props;
  const [timeLeft, setTimeLeft] = useState(ROUND_LENGTH);

  function reset() {
    setTimeLeft(ROUND_LENGTH);
  }

  useEffect(() => {
    let interval = null;
    if (isTimerStarted) {
      interval = setInterval(() => {
        setTimeLeft(timeLeft => Math.max(timeLeft - 1, 0));
      }, 1000);
    } else if (!isTimerStarted) {
      clearInterval(interval);
      setTimeLeft(ROUND_LENGTH);
    }
    return () => clearInterval(interval);
  }, [isTimerStarted]);

  return (
    <Container className='timer-container'>
      <div className="time">
        {timeLeft}s
      </div>
    </Container>
  );
};
