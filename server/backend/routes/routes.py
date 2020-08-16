# from flask import session, redirect, url_for, render_template, request
from . import routes_blueprint

@routes_blueprint.route('/', methods=['GET'])
def test():
  return {
    'test': True
  }