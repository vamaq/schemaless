#!/usr/bin/env python

from distutils.core import setup

setup(name='model',
    version='1.0',
    description='RDBMS SQLAlchemy models definition',
    py_modules=['model'],
    install_requires=['sqlalchemy','psycopg2'],
    )
