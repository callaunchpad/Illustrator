import React from 'react'
/**
 * A global context object. Components can access elements in this context object
 * by calling React.useContext(GlobalContext) in the functional component. Make
 * sure that GlobalContext is imported from context.js before trying to do so.
 * 
 * The values of this object are determiend by the App component
 */
const GlobalContext = React.createContext({});

export default GlobalContext;