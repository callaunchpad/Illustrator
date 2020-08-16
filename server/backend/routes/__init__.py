from flask import Blueprint

routes_blueprint = Blueprint('routes_blueprint', __name__)

# all route handlers are defined in routes.py file
from . import routes