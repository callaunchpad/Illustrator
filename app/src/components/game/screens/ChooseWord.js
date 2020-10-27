import React from 'react'

export default function ChooseWord(props) {
  return (
    <div className='chooseWord container'>
      <ul>
        {props.choices.map((word, idx) => {
          return (
            <li key={idx} style={{color: 'white'}}>
              {word}
            </li>
          );
        })}
      </ul>
    </div>
  )
}
