import logging
from flask import _app_ctx_stack, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.event import listen

from config import config

SESSION = None
DB_HITS = 0
LOGGER = logging.getLogger(__name__)


def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """ Do that things you would like to do before hitting the DB
    """
    global DB_HITS
    DB_HITS = DB_HITS +1


def init_app(app):
    app.teardown_appcontext(close_database_connection)
    app.teardown_request(teardown_request)
    app.before_request(before_request)

    engine = create_engine(config["SQLALCHEMY_URL"], connect_args={"application_name":"schemasless"})

    # Keep some insight on the interaction with the DB.
    listen(engine, "before_cursor_execute", before_cursor_execute)

    global SESSION  # pylint: disable=global-statement
    SESSION = scoped_session(sessionmaker(
        bind=engine, autoflush=False), scopefunc=_app_ctx_stack.__ident_func__)
    

def close_database_connection(error=None):
    """ To be called when the application context ends.
    """
    SESSION.close()
    if error:
        LOGGER.error('Error while closing the app: %s', str(error))


def before_request():
    global DB_HITS
    DB_HITS = 0

    if not hasattr(g, 'db_session'):
        g.db_session = SESSION()


def teardown_request(exception):
    if exception:
        SESSION.rollback()
    # Commit the changed to the database
    SESSION.commit()
    # This will close the current db session
    SESSION.close()
    SESSION.remove()

    LOGGER.info('Hits to the DB: %s', str(DB_HITS))
