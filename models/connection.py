import os
import psycopg2
import psycopg2.extras as extras

from config.db import db_uri


class Connection:

    def __init__(self):
        if os.environ.get("APP_ENV") == "development":
            self.db_string = db_uri.get("dev_db")

        elif os.environ.get("APP_ENV") == "testing":
            self.db_string = db_uri.get("test_db")
        else:
            self.db_string = db_uri.get("prod_db")

    def connect(self):
        try:
            #  Create a connection object
            conn = psycopg2.connect(self.db_string)
            conn.autocommit = True
            #  Create a cursor
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            return cursor

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
