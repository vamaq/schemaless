import os


config = {
    "SQLALCHEMY_URL": "postgresql://postgres:postgres@127.0.0.1/postgres"
}


def init():
    """ This function executes on import, so be careful with it.
    """
    for k in config.keys():
        if k in os.environ:
            config[k] = os.getenv(k)
