
import ssl
from os import path
cwd = path.dirname(path.realpath(__file__))
from aiohttp import web
from backend import app

ssl_dir = 'ssl'
ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain(path.join(cwd, ssl_dir, 'domain_srv.crt'), path.join(cwd, ssl_dir, 'domain_srv.key'))
if __name__ == '__main__':
  web.run_app(app, port=5000) # ssl_context=ssl_context)
