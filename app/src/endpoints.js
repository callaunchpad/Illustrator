/**
 * Contains all the endpoints the application will need. You can 
 * import the ENDPOINTS object, and then do ENDPOINTS.<endpoint>
 * to get the endpoint string. Feel free to add more endpoints here.
 */

const dev = true
const serverUrl = dev ? 'http://127.0.0.1:5000/' : ''
const ENDPOINTS = {
  root: `${serverUrl}`,
  test: `${serverUrl}/test`,
  game: `${serverUrl}/game`
}
export default ENDPOINTS