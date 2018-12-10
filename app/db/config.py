import psycopg2
import os

# base db url
base_url = os.getenv('DATABASE_URL')
# dsn = "dbname=ireporter user=user password=password host=localhost"

# test db url
test_url = "dbname=ireporter_testdb host=localhost port=5432 user=elishamisoi password=postgres"

# returns connection for base db


def init_db():
    try:
        return psycopg2.connect(base_url)
    except BaseException:
        print("Unable to establish connection to database")

# returns connection for test db


def init_test_db():
    try:
        return psycopg2.connect(test_url)
    except BaseException:
        print("Unable to establish connection to database")


def open_connection():
    # opening connection for base db queries
    conn = init_db()
    return conn


def open_testDb_connection():
    # opening connection for test db queries
    conn = init_test_db()
    return conn


def close_connection(conn):
    # closing connection after queries
    conn.commit()
    conn.close()
