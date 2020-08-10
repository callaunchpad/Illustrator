const dev = true
const serverUrl = dev ? 'http://127.0.0.1:5000/' : ''
const ENDPOINTS = {
  root: `${serverUrl}`,
  test: `${serverUrl}/test`
}
export default ENDPOINTS