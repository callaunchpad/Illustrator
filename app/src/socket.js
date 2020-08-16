import socketIOClient from "socket.io-client";
import ENDPOINTS from './endpoints';

// global constant socket instance
const socket = socketIOClient(ENDPOINTS.root);
export default socket