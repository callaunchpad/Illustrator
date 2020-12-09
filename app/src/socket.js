/**
 * contains the app's global socket instance that
 * establishes connection with our server. To import it
 * you can do "import socket from <path_to_this_file>"
 */

import socketIOClient from "socket.io-client";
import ENDPOINTS from './endpoints';

// global constant socket instance
const socket = socketIOClient(ENDPOINTS.root);
export default socket