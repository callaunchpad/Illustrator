from backend import app, socketio
import unittest
import json
class SampleTestCase(unittest.TestCase):
  # def test_simple_get(self):
  #   print("TEST_SIMPLE_GET\n")
  #   tester = app.test_client(self)
  #   response = tester.get('/')
  #   self.assertEqual(response.status_code, 200)
  #   response_json = json.loads(response.data)
  #   print("response data is: ", response_json)
  #   self.assertTrue(response_json['test'])

  def test_simple_socket_msg(self):
    print("TEST_SIMPLE_SOCKET_MSG\n")
    app_tester = app.test_client(self)
    socket_tester = socketio.test_client(app, flask_test_client=app_tester)
    socket_tester.emit('create_game', {'roomId': 1, "num_rounds":4})
    recvd = socket_tester.get_received()
    print('recvd list looks like this after create_game', recvd)
    print()

    app_tester2 = app.test_client(self)
    socket_tester2 = socketio.test_client(app, flask_test_client=app_tester2)
    socket_tester2.emit('join', {'roomId': 1, 'username': "player1"})
    recvd2 = socket_tester2.get_received()
    recvd = socket_tester.get_received()
    # the recvd response contains information pertaining to what the server sends to the client
    # in response to a socket message
    print('recvd list looks like this after join:', recvd)
    print()
    print('recvd2 list looks like this after join:', recvd2)
    print()
    # recvd3 = socket_tester2.get_received()
    # print('recvd3 list looks like this after join:', recvd3)
    # print()

    socket_tester.emit('send_guess', {'roomId': 1, "guess":"dog"})
    recvd = socket_tester.get_received()
    print('recvd list looks like this after send_guess:', recvd)
    print()
    self.assertEqual(recvd[0]['args'][0], {'roomId': 1, "guess":"dog"})

    socket_tester.emit("start_game", {'roomId': 1})
    recvd = socket_tester.get_received()
    print('recvd list looks like this after start_game:', recvd)


  def test_create_game(self):
    print("TEST_CREATE_GAME\n")
    app_tester = app.test_client(self)
    socket_tester = socketio.test_client(app, flask_test_client=app_tester)
    # the recvd response contains information pertaining to what the server sends to the client
    # in response to a socket message
    socket_tester.emit('create_game', {'roomId': 1, "num_rounds":4})
    recvd = socket_tester.get_received()
    print('recvd list looks like this after create_game', recvd)
    print()


    


if __name__ == "__main__":
  unittest.main()
