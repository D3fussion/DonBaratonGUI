import psycopg2


def get_db_connection():
    conn = psycopg2.connect("postgresql://DonBaraton_owner:FzYT6uwqL8ek@ep-wispy-bird-a4q98q3x.us-east-1.aws.neon.tech/DonBaraton?sslmode=require")
    return conn
