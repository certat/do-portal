#!venv/bin/env python
import os
import pymysql
from app import celery, create_app  # noqa

pymysql.install_as_MySQLdb()

app = create_app(os.getenv('DO_CONFIG') or 'default')
app.app_context().push()
