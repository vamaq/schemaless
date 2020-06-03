import random
import string

from flask import Flask, request

from config import config
from db import init_app as db_init_app

from api.v1 import get_api_v1

def before_request():
    # TODO: Need to properly handle session, CSRF, etc.
    pass


def initialize_app():
    """ Initialize app
    """
    app = Flask(__name__)

    # Initialize config
    app.config.from_object(config)

    # Initialize Database
    # Contains a before_request call
    db_init_app(app)

    # Request scoped values
    app.before_request(before_request)

    # Initialize APIs
    app.register_blueprint(get_api_v1())

    return app


if __name__ == '__main__':
    app = initialize_app()
    app.run(host='0.0.0.0', debug=True, port='8090', threaded=False)
