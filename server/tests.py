from backend import app, socketio
import unittest
import json
class SampleTestCase(unittest.TestCase):
  def test_simple_get(self):
    tester = app.test_client(self)
    response = tester.get('/')
    self.assertEqual(response.status_code, 200)
    response_json = json.loads(response.data)
    print("response data is: ", response_json)
    self.assertTrue(response_json['test'])

  def test_simple_socket_msg(self):
    app_tester = app.test_client(self)
    socket_tester = socketio.test_client(app, flask_test_client=app_tester)
    socket_tester.emit('join', {'roomId': 1})
    recvd = socket_tester.get_received()
    # the recvd response contains information pertaining to what the server sends to the client
    # in response to a socket message
    print('recvd list looks like this after join:', recvd)
    socket_tester.emit('send_guess', {'roomId': 1})
    recvd = socket_tester.get_received()
    print('recvd list looks like this after send_guess:', recvd)
    self.assertEqual(recvd[0]['args'][0], {'roomId': 1})

if __name__ == "__main__":
  unittest.main()