# from flask import session, redirect, url_for, render_template, request
from flask import render_template, redirect, request, url_for
from . import routes_blueprint
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
def home(req):
  print("root get request")
  # return render_template('index.html')
  # return home template
  # home template should have input for username and roomId
  # should have two buttons, create room and join room
  # connect socket events to the buttons: create_game and join

# define whether this is for creating or joining a game from the home page
@routes.post('/game')
async def game(req):
  body = await req.json()
  username = body.get('username')
  roomId = body.get('roomId')
  response = {'join': username and roomId, 'create': username and True}
  return web.json_response(response)
