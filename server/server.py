
from aiohttp import web
from backend import app

if __name__ == '__main__':
  web.run_app(app, port=5000)