import psycopg2
import psycopg2.extras

from flask import current_app, g

def get_conn():
    if 'conn' not in g:
        g.conn = psycopg2.connect(
            user=current_app.config['DB_USERNAME'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=int(current_app.config['DB_PORT']),
            dbname=current_app.config['DB_DATABASE'],
        )

    return g.conn

def get_curs(conn):
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return curs

def close_conn(e=None):
    conn = g.pop('conn', None)

    if conn is not None:
        conn.close()

def init_app(app):
    app.teardown_appcontext(close_conn)