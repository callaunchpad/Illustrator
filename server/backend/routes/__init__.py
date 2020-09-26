from flask import Blueprint

routes_blueprint = Blueprint('routes_blueprint', __name__)

# all http request route handlers are defined in routes.py file. In other words,
# all the logic that goes into handling requests from the client will be defined there
from . import routes