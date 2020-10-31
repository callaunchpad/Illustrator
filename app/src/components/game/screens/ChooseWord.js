import React from 'react'

export default function ChooseWord(props) {
  return (
    <div className='chooseWord container'>
      <ul>
        {props.choices.map((word, idx) => {
          return (
            <li
              key={idx}
              style={{color: 'black', cursor: 'pointer'}}
              onClick={(e) => {
                e.preventDefault();
                props.onChooseWord(word);
              }}
            >
              {word}
            </li>
          );
        })}
      </ul>
    </div>
  )
}
