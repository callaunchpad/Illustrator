from flask import render_template, redirect, request, url_for
from . import routes_blueprint
from aiohttp import web

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
  response = {'join': username and roomId, 'create': username and True}
  return web.json_response(response)
