import os


db_uri = {
    "test_db": "dbname='posdb' user='postgres' host='localhost' password='snOOkg'",
    "dev_db": "dbname='storedb' user='postgres' host='localhost' password='snOOkg'",
    "prod_db": os.environ.get("DATABASE_URL")
}
