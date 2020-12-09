from aiohttp import web
from flask import render_template, redirect, request, url_for

from . import routes_blueprint
from ..globals import ROOMS_GAMES, PlAYER_TO_GAME, ROOM_USERNAMES

routes = web.RouteTableDef()

@routes.get('/')
def home(req):
  print("root get request")

# define whether this is for creating or joining a game from the home page
@routes.post('/game')
async def game(req):
  body = await req.json()
  username = body.get('username')
  roomId = body.get('roomId')
  print(ROOM_USERNAMES)
  response = {
    'too_many': len(ROOM_USERNAMES[roomId]) > 8,
    'duplicate': username in ROOM_USERNAMES[roomId],
    'join': username and roomId,
    'create': username and not roomId,
    'username': username,
    'roomId': roomId
  }
  return web.json_response(response)
