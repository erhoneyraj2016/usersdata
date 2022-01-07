import sqlite3

conn = sqlite3.connect('datas.sqlite')

cursor = conn.cursor()
sql_query = """CREATE TABLE data(
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    company_name text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip text NOT NULL,
    email text NOT NULL,
    web text NOT NULL,
    age text NOT NULL
)"""
cursor.execute(sql_query)

