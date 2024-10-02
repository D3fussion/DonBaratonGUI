import psycopg2

SQL = os.getenv("MY_SQL")

def get_db_connection():
    conn = psycopg2.connect(SQL)
    return conn
