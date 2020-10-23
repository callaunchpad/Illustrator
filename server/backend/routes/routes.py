# from flask import session, redirect, url_for, render_template, request
from flask import render_template, redirect, request, url_for
from . import routes_blueprint

# @routes_blueprint.route('/', methods=['GET'])
# def test():
#   return {
#     'test': True
#   }

@routes_blueprint.route('/', methods=['GET'])
def home():
  return render_template('index.html')
  # return home template
  # home template should have input for username and roomId
  # should have two buttons, create room and join room
  # connect socket events to the buttons: create_game and join

# define whether this is for creating or joining a game from the home page
@routes_blueprint.route('/game', methods=['POST'])
def game():
  print("request is: ", request)
  username = request.json.get('username')
  roomId = request.json.get('roomId')
  if username and roomId:
    return {
      'success': True,
    }
  # if username and roomId:
  #   return render_template('game_room.html', username=username, room=roomId)
  # return redirect(url_for('routes_blueprint.home'))
