import aiohttp_cors
from aiohttp import web

import run
# import lstm_run

routes = web.RouteTableDef()
@routes.get('/')
async def root(req):
  print("got request!")
# define whether this is for creating or joining a game from the home page
@routes.post('/classify')
async def classify(req):
  print("got classification request!")
  body = await req.json()
  word = body.get('word')
  strokes = body.get('strokes')
  pred = run.classify(strokes)
  # pred = lstm_run.classify(strokes)
  response = {'pred': pred}
  return web.json_response(response)

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
      allow_credentials=True,
      expose_headers="*",
      allow_headers="*",
    ),
})
app_routes = app.add_routes(routes)
for route in app_routes:
  cors.add(route)

if __name__ == '__main__':
  web.run_app(app, port=8080)
